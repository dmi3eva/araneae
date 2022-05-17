from typing import *
import pandas as pd
from random import choice
from araneae.wrapper import Araneae
from configure import *
from dto.sample import *
from utils.spider_connectors import *

AMOUNT = 10


def get_inds(araneae: Araneae) -> Tuple[List[int], List[int], List[int]]:
    samples = araneae.samples.content
    train_inds = [i for i, s in enumerate(samples) if s.source is Source.SPIDER_TRAIN]
    train_others_inds = [i for i, s in enumerate(samples) if s.source is Source.SPIDER_TRAIN_OTHERS]
    test_inds = [i for i, s in enumerate(samples) if s.source is Source.SPIDER_DEV]
    return train_inds, train_others_inds, test_inds


def sample_with_values(araneae: Araneae, inds: List[int], amount: int) -> List[Dict]:
    en_spider = EnSpiderDB()
    ru_spider = RuSpiderDB()
    chosen_inds = []
    samples = araneae.samples.content
    chosen_samples = []
    while len(chosen_samples) < amount:
        ind = choice(inds)
        sample = samples[ind]
        mentions_where = list(filter(lambda x: x.type is Subquery.WHERE, sample.mentions))
        if ind not in chosen_inds and len(mentions_where) > 0:
            mention = mentions_where[0]
            chosen_inds.append(ind)
            en_all_values = en_spider.get_values(mention.db, mention.table, mention.column)
            ru_all_values = ru_spider.get_values(mention.db, mention.table, mention.column)
            sample_json = {
                "id": sample.id,
                "en": sample.question,
                "ru": sample.russian_question,
                "sql_en": sample.query,
                "sql_ru": sample.russian_query,
                "db_id": sample.db_id,
                "ru_corrected": "",
                "sql_ru_corrected": "",
                "source": sample.source.value,
                "type": "empty",
                "tag": "",
                "db": mention.db,
                "table": mention.table,
                "column": mention.column,
                "en_values": str(sorted(list(set(en_all_values)))),
                "ru_values": str(sorted(list(set(ru_all_values))))
            }
            chosen_samples.append(sample_json)
    return chosen_samples


def generate_random_samples(araneae: Araneae, filename: str, amount: int) -> NoReturn:
    train_inds, train_others_inds, test_inds = get_inds(araneae)
    train_inds_sample = sample_with_values(araneae, train_inds, amount)
    train_others_inds_sample = sample_with_values(araneae, train_others_inds, amount)
    test_inds_sample = sample_with_values(araneae, test_inds, amount)
    data = train_inds_sample + train_others_inds_sample + test_inds_sample
    df = pd.DataFrame(data=data)
    df.to_csv(filename, encoding='utf-8')


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    generate_random_samples(araneae, EMPTY_SAMPLES, 20)
