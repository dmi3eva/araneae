from collections import Counter
from utils.spider_connectors import *
from dto.sample import *
from utils.spider_analysis import *
from araneae.wrapper import Araneae
from dataclasses import dataclass


@dataclass
class Representative:
    value: int
    examples: Optional[List[Sample]]


def get_mentions_sizes_statistic(araneae: Araneae) -> Tuple[Representative, Dict]:
    statistics = {}
    max_size_representative = Representative(value=0, examples=None)
    for sample in araneae.samples.content:
        all_mentions = sample.mentions
        for mention in all_mentions:
            all_values = mention.values
            if not all_values:
                continue
            for value in all_values:
                size = len(str(value))
                statistics[size] = statistics.get(size, 0) + 1
                if size > max_size_representative.value:
                    max_size_representative = Representative(size, [sample])
                if size == max_size_representative.value:
                    max_size_representative.examples.append(sample)
    return max_size_representative, statistics



if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    en_symbols, ru_symbols, en_tokens, ru_tokens = get_mentions_sizes_statistic(araneae)
    a = 7