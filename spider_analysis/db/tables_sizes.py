from collections import Counter
from utils.spider_connectors import *
from dataclasses import dataclass


@dataclass
class NumericalItem:
    key: Union[int, str]
    value: int


class NumericalStatistics:
    def __init__(self, content: Counter):
        sorted_items = sorted(content.items())
        self.content = [NumericalItem(key=_k, value=_v) for _k, _v in sorted_items]

    def get_x(self):
        return [_item.key for _item in self.content]

    def get_y(self):
        return [_item.value for _item in self.content]


def get_tables_sizes_statistics(connector: SpiderDB) -> Tuple[NumericalStatistics, NumericalStatistics]:
    all_sizes = []
    unique_sizes = []
    for _triple in connector.triples:
        db, table, column = _triple
        values = connector.get_values(db, table, column)
        unique_values = set(values)
        all_sizes.append(len(values))
        unique_sizes.append(len(unique_values))
    all_counter = Counter(all_sizes)
    unique_counter = Counter(unique_sizes)
    return NumericalStatistics(all_counter), NumericalStatistics(unique_counter)