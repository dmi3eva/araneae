from dataclasses import dataclass
from typing import *


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