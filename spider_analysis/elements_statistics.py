from typing import *
import json
import pandas as pd
from copy import deepcopy
from araneae.wrapper import Araneae
from araneae.settings import *
from dto.sample import *


def make_join_statistic(samples: List[Sample]):
    statistics = {}
    statistics_dev = {}
    statistics_train = {}
    for _sample in samples:
        join_toks = [_t for _t in _sample.query_toks if _t.lower() == 'join']
        amount = len(join_toks)
        statistics[amount] = statistics.get(amount, 0) + 1
        if _sample.type is TrainDevType.TRAIN:
            statistics_train[amount] = statistics_train.get(amount, 0) + 1
        else:
            statistics_dev[amount] = statistics_dev.get(amount, 0) + 1
    return statistics, statistics_train, statistics_dev


def make_agg_statistic(samples: List[Sample]):
    statistics = {
        'min': 0,
        'max': 0,
        'avg': 0,
        'sum': 0,
        'count': 0
    }
    statistics_dev = deepcopy(statistics)
    statistics_train = deepcopy(statistics)
    for _sample in samples:
        toks = [_t.lower() for _t in _sample.query_toks]
        for _k, _v in statistics.items():
            if _k in toks:
                statistics[_k] += 1
                if _sample.type is TrainDevType.TRAIN:
                    statistics_train[_k] += 1
                else:
                    statistics_dev[_k] += 1
    return statistics, statistics_train, statistics_dev


def save_elements_statistics(statistics, filename):
    with open(f"../resources/results/statistics/{filename}.json", 'w') as f:
        json.dump(statistics, f)

    data = [{"Elements": str(_s), "Amount": _a} for _s, _a in statistics.items()]
    df = pd.DataFrame(data=data)
    df.to_csv(f"../resources/results/statistics/{filename}.csv")


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    statistics_agg, train_agg, dev_agg = make_agg_statistic(araneae.samples.content)
    statistics_join, train_join, dev_join = make_join_statistic(araneae.samples.content)
    save_elements_statistics(statistics_agg, "22_06_23_agg")
    save_elements_statistics(train_agg, "22_06_23_train_agg")
    save_elements_statistics(dev_agg, "22_06_23_dev_agg")
    save_elements_statistics(statistics_join, "22_06_23_join")
    save_elements_statistics(train_join, "22_06_23_train_join")
    save_elements_statistics(dev_join, "22_06_23_dev_join")
    a = 7