from typing import *
import pandas as pd
from random import choice
from araneae.wrapper import Araneae
from configure import *
from dto.sample import *
from spider_analysis.db.tables_sizes import is_russian
from dataclasses import dataclass
from utils.spider_connectors import *

ENGLISH_THRESHOLD = 21
RUSSIAN_THRESHOLD = 5

@dataclass
class Value:
    db: str
    table: str
    column: str
    value: str


def extract_long_value(threshold: int, connector: SpiderDB, language: Language) -> List[Value]:
    appropriate_values = []
    if language is Language.RU:
        connector = RuSpiderDB()
    else:
        connector = EnSpiderDB()
    for _triple in connector.triples:
        db, table, column = _triple
        all_values = connector.get_values(db, table, column)
        if language is Language.RU:
            all_values = list(filter(is_russian, all_values))
        appropriate_values += [
            Value(db=db, table=table, column=column, value=_v) for _v in all_values if len(_v.split()) > threshold
        ]
    return appropriate_values


def sample_with_values(araneae: Araneae, inds: List[int], amount: int) -> List[Dict]:
    chosen_inds = []
    samples = araneae.samples.content
    chosen_samples = []
    while len(chosen_samples) < amount:
        ind = choice(inds)
        sample = samples[ind]
        mention_types = [m.type for m in sample.mentions]
        if ind not in chosen_inds and Subquery.WHERE in mention_types:
            chosen_inds.append(ind)
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
                "tag": ""
            }
            chosen_samples.append(sample_json)
    return chosen_samples


def generate_long_english_samples(araneae: Araneae, filename: str, threshold: int) -> NoReturn:
    samples = araneae.samples.content


def generate_long_russian_samples(araneae: Araneae, filename: str, threshold: int) -> NoReturn:
    pass


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    generate_long_english_samples(araneae, LONG_ENGLISH_SAMPLES, ENGLISH_THRESHOLD)
    generate_long_russian_samples(araneae, LONG_RUSSIAN_SAMPLES, RUSSIAN_THRESHOLD)
