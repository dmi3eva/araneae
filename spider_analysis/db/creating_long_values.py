from typing import *
import pandas as pd
import json
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
    for ind, _triple in enumerate(connector.triples):
        if ind % 100 == 0:
            print(f"{ind} / {len(connector.triples)}")
        db, table, column = _triple
        all_values = connector.get_values(db, table, column)
        if language is Language.RU:
            all_values = list(filter(is_russian, all_values))
        appropriate_values += [
            Value(db=db, table=table, column=column, value=_v) for _v in all_values if len(_v.split()) >= threshold
        ]
    return appropriate_values


def make_dict(long_values: List[Value]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    values_dict = {}
    for long in long_values:
        if long.db not in values_dict.keys():
            values_dict[long.db] = {}
        if long.table not in values_dict[long.db].keys():
            values_dict[long.db][long.table] = {}
        if long.column not in values_dict[long.db][long.table].keys():
            values_dict[long.db][long.table][long.column] = []
        values_dict[long.db][long.table][long.column].append(long.value)
        values_dict[long.db][long.table][long.column] = list(set(values_dict[long.db][long.table][long.column]))
    return values_dict


def extract_requests(araneae: Araneae, long_dict: Dict, filename: str, language: Language) -> NoReturn:
    samples = araneae.samples.content
    chosen_samples = []
    chosen_ids = set()
    for _sample in samples:
        if language is Language.EN:
            mentions = _sample.mentions
        else:
            mentions = _sample.russian_mentions
        for _mention in mentions:
            if _mention.db in long_dict.keys() and _mention.table in long_dict[_mention.db].keys():
                sample_json = {
                    "id": _sample.id,
                    "en": _sample.question,
                    "ru": _sample.russian_question,
                    "sql_en": _sample.query,
                    "sql_ru": _sample.russian_query,
                    "db_id": _sample.db_id,
                    "ru_corrected": "",
                    "sql_ru_corrected": "",
                    "source": _sample.source.value,
                    "type": "empty",
                    "tag": "",
                    "db": _mention.db,
                    "table": _mention.table,
                    "columns_and_values": str(long_dict[_mention.db][_mention.table])
                }
                chosen_samples.append(sample_json)
                chosen_ids.add(_sample.id)
                break
    df = pd.DataFrame(data=chosen_samples)
    df.to_csv(filename, encoding='utf-8')
    return chosen_samples


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    en_spider = EnSpiderDB()
    ru_spider = RuSpiderDB()
    long_en_values = extract_long_value(20, en_spider, Language.EN)
    long_ru_values = extract_long_value(9, ru_spider, Language.RU)

    long_en_dict = make_dict(long_en_values)
    long_ru_dict = make_dict(long_ru_values)

    with open(LONG_EN_SAMPLES_JSON, "w", encoding='utf-8') as out_json:
        json.dump(long_en_dict, out_json)
    with open(LONG_RU_SAMPLES_JSON, "w", encoding='utf-8') as out_json:
        json.dump(long_ru_dict, out_json)

    extract_requests(araneae, long_en_dict, LONG_EN_SAMPLES_CSV, Language.EN)
    extract_requests(araneae, long_ru_dict, LONG_RU_SAMPLES_CSV, Language.RU)

