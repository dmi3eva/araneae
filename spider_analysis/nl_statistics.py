import json
from typing import *
import pandas as pd

from configure import *
from dto.sample import *
from araneae.wrapper import Araneae


def make_nl_frequency_statistics(samples: List[Sample], ignore_agg=True) -> Dict[str, int]:
    statistics = {}
    for _sample in samples:
        for _token in _sample.question_toks:
            processed = _token.lower()
            statistics[processed] = statistics.get(processed, 0) + 1
    return statistics


def save_nl_statistics(statistics, filename):
    with open(f"../resources/results/statistics/{filename}.json", 'w') as f:
        json.dump(statistics, f)

    data = [{"Token": str(_s), "Amount": _a} for _s, _a in statistics.items()]
    df = pd.DataFrame(data=data)
    df = df.sort_values(["Amount"], ascending=False)
    df.to_csv(f"../resources/results/statistics/{filename}.csv")


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    nl_frequency = make_nl_frequency_statistics(araneae.samples.content, ignore_agg=False)
    save_nl_statistics(nl_frequency, "09_03_25_nl_frequency")
    a = 7
