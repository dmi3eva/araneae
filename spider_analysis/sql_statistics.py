from typing import *
import json
import pandas as pd
from copy import deepcopy
from araneae.wrapper import Araneae
from araneae.settings import *
from dto.sample import *

FILLER = '<ent>'


def extract_sql_structure(sql_tokens: List[str], service_words: List[str]) -> List[str]:
    sql_structure = []
    for _token in sql_tokens:
        if _token.lower() in service_words:
            sql_structure.append(_token.upper())
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


def make_sql_statistic(samples: List[Sample], ignore_agg=True) -> Dict[str, int]:
    statistics = {}
    service_words = deepcopy(KEY_WORDS)
    if not ignore_agg:
        service_words += AGGREGATIONS
    for _sample in samples:
        sql_structure = extract_sql_structure(_sample.query_toks, service_words)
        sql_pattern = " ".join(sql_structure)
        statistics[sql_pattern] = statistics.get(sql_pattern, 0) + 1
    return statistics


def save_sql_statistics(statistics, filename):
    with open(f"../resources/results/statistics/{filename}.json", 'w') as f:
        json.dump(statistics_with_agg, f)

    data = [{"SQL-structure": str(_s), "Amount": _a} for _s, _a in statistics.items()]
    df = pd.DataFrame(data=data)
    df.to_csv(f"../resources/results/statistics/{filename}.csv")


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    statistics_with_agg = make_sql_statistic(araneae.samples.content, ignore_agg=False)
    statistics_without_agg = make_sql_statistic(araneae.samples.content)
    save_sql_statistics(statistics_with_agg, "22_02_25_with_agg")
    save_sql_statistics(statistics_without_agg, "22_02_25_without_agg_brackets")
    a = 7