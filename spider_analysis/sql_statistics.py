from typing import *
import json
import pandas as pd
from araneae.wrapper import Araneae
from araneae.settings import *
from dto.sample import *

FILLER = '<ent>'


def extract_sql_structure(sql_tokens: List[str], ignore_agg=True) -> List[str]:
    sql_structure = []
    service_words = KEY_WORDS
    if not ignore_agg:
        service_words += AGGREGATIONS
    for _token in sql_tokens:
        if _token.lower() in KEY_WORDS:
            sql_structure.append(_token)
        else:
            sql_structure.append(FILLER)
    sql_structure = postprocess(sql_structure)
    return sql_structure


def postprocess(sql_structure: List[str]) -> List[str]:
    processed = ["START"]
    for ind, element in enumerate(sql_structure):
        if element != FILLER or element != processed[-1]:
            processed.append(element)
    return processed[1:]


def make_statistic(samples: List[Sample]) -> Dict[str, int]:
    statistics = {}
    for _sample in samples:
        sql_structure = extract_sql_structure(_sample.query_toks)
        sql_pattern = " ".join(sql_structure)
        # print(_sample.query)
        # print(sql_structure)
        # print("------------")
        statistics[sql_pattern] = statistics.get(sql_pattern, 0) + 1
    return statistics


def save_statistics(statistics, filename):
    with open(f"../resources/results/statistics/{filename}.json", 'w') as f:
        json.dump(statistics_with_agg, f)

    data = [{"SQL-structure": _s, "Amount": _a} for _s, _a in statistics.items()]
    df = pd.DataFrame(data=data)
    df.to_csv(f"../resources/results/statistics/{filename}.csv")


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    statistics_with_agg = make_statistic(araneae.samples.content)
    statistics_without_agg = make_statistic(araneae.samples.content)
    save_statistics(statistics_with_agg, "22_02_24_with_agg")
    save_statistics(statistics_without_agg, "22_02_24_without_agg")
    a = 7