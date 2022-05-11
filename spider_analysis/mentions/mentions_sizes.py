from collections import Counter
from utils.spider_connectors import *
from dto.sample import *
from utils.spider_analysis import *
from araneae.wrapper import Araneae
from dataclasses import dataclass
from spider_analysis.db.tables_sizes import is_russian


@dataclass
class Representative:
    value: int
    examples: Optional[List[Sample]]


def get_mentions_symbols_statistic(araneae: Araneae) -> Tuple[Representative, Dict]:
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


def get_mentions_tokens_statistic(araneae: Araneae) -> Tuple[Representative, Dict]:
    statistics = {}
    max_size_representative = Representative(value=0, examples=None)
    for sample in araneae.samples.content:
        all_mentions = sample.mentions
        for mention in all_mentions:
            all_values = mention.values
            if not all_values:
                continue
            for value in all_values:
                size = len(str(value).split())
                statistics[size] = statistics.get(size, 0) + 1
                if size > max_size_representative.value:
                    max_size_representative = Representative(size, [sample])
                if size == max_size_representative.value:
                    max_size_representative.examples.append(sample)
    return max_size_representative, statistics


def get_russian_mentions_symbols_statistic(araneae: Araneae) -> Tuple[Representative, Dict]:
    statistics = {}
    max_size_representative = Representative(value=0, examples=None)
    for sample in araneae.samples.content:
        all_mentions = sample.russian_mentions
        for mention in all_mentions:
            all_values = mention.values
            if not all_values:
                continue
            for value in all_values:
                if not is_russian(str(value)):
                    continue
                size = len(str(value))
                statistics[size] = statistics.get(size, 0) + 1
                if size > max_size_representative.value:
                    max_size_representative = Representative(size, [sample])
                if size == max_size_representative.value:
                    max_size_representative.examples.append(sample)
    return max_size_representative, statistics


def get_russian_mentions_tokens_statistic(araneae: Araneae) -> Tuple[Representative, Dict]:
    statistics = {}
    max_size_representative = Representative(value=0, examples=None)
    for sample in araneae.samples.content:
        all_mentions = sample.russian_mentions
        for mention in all_mentions:
            all_values = mention.values
            if not all_values:
                continue
            for value in all_values:
                if not is_russian(str(value)):
                    continue
                size = len(str(value).split())
                statistics[size] = statistics.get(size, 0) + 1
                if size > max_size_representative.value:
                    max_size_representative = Representative(size, [sample])
                if size == max_size_representative.value:
                    max_size_representative.examples.append(sample)
    return max_size_representative, statistics



if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    max_symbols_representative, symbols_statistics = get_mentions_symbols_statistic(araneae)
    max_tokens_representative, tokens_statistics = get_mentions_tokens_statistic(araneae)
    max_russian_symbols_representative, russian_symbols_statistics = get_russian_mentions_symbols_statistic(araneae)
    max_russian_tokens_representative, russian_tokens_statistics = get_russian_mentions_tokens_statistic(araneae)
    a = 7