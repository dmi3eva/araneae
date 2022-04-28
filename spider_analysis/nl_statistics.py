import json
from typing import *
import pandas as pd

from configure import *
from dto.sample import *
from araneae.wrapper import Araneae


def make_nl_frequency_statistics(samples: List[Sample], language: Language, ignore_agg=True) -> Dict[str, int]:
    statistics = {}
    for _sample in samples:
        if language is Language.EN:
            tokens = _sample.question_toks
        else:
            tokens = _sample.russian_question_toks
        for _token in tokens:
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
    nl_frequency = make_nl_frequency_statistics(araneae.samples.content, Language.EN, ignore_agg=False)
    save_nl_statistics(nl_frequency, "22_04_28_nl_frequency_en")
    a = 7
