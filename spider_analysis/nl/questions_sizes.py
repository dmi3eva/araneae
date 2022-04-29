from collections import Counter
from utils.spider_connectors import *
from utils.spider_analysis import *
from araneae.wrapper import Araneae



def get_nl_sizes_statistics(araneae) -> Tuple[NumericalStatistics, NumericalStatistics, NumericalStatistics, NumericalStatistics]:
    """
    Returns sizes of qestions in symbols and in tokens
    """

    # TODO: Turn it for excersice for students in refactoring :)

    longest_symbols_en = ""
    longest_symbols_ru = ""

    longest_tokens_en = []
    longest_tokens_ru = []

    all_english_symbols = []
    all_russian_symbols = []

    all_english_tokens = []
    all_russian_tokens = []

    for ind, sample in enumerate(araneae.samples.content):
        # if ind in [6196, 6197, 9134, 9692]:
        #     continue
        english_nl = sample.question
        russian_nl = sample.russian_question
        english_tokens = sample.question_toks
        russian_tokens = sample.russian_question_toks
        all_english_symbols.append(len(english_nl))
        all_russian_symbols.append(len(russian_nl))
        all_english_tokens.append(len(english_tokens))
        all_russian_tokens.append(len(russian_tokens))
        if len(english_nl) > len(longest_symbols_en):
            longest_symbols_en = english_nl
        if len(russian_nl) > len(longest_symbols_ru):
            longest_symbols_ru = russian_nl
        if len(english_tokens) > len(longest_tokens_en):
            longest_tokens_en = english_tokens
        if len(russian_tokens) > len(longest_tokens_ru):
            longest_tokens_ru = russian_tokens
        if russian_nl.startswith("SELECT"):
            a = 7

    print(f"Longest english, tokens:\n {' '.join(longest_tokens_en)} ({len(longest_tokens_en)})")
    print(f"Longest russian, tokens:\n {' '.join(longest_tokens_ru)} ({len(longest_tokens_ru)})")

    print(f"Longest english, symbols:\n {longest_symbols_en} ({len(longest_symbols_en)})")
    print(f"Longest russian, symbols:\n {longest_symbols_ru} ({len(longest_symbols_ru)})")

    print(f"Average english, symbols:\n {sum(all_english_symbols) / len(all_english_symbols)}")
    print(f"Average russian, symbols:\n {sum(all_russian_symbols) / len(all_russian_symbols)}")

    print(f"Average english, tokens:\n {sum(all_english_tokens) / len(all_english_tokens)}")
    print(f"Average russian, tokens:\n {sum(all_russian_tokens) / len(all_russian_tokens)}")

    en_symbols_counter = Counter(all_english_symbols)
    ru_symbols_counter = Counter(all_russian_symbols)

    en_tokens_counter = Counter(all_english_tokens)
    ru_tokens_counter = Counter(all_russian_tokens)

    return NumericalStatistics(en_symbols_counter), \
           NumericalStatistics(ru_symbols_counter), \
           NumericalStatistics(en_tokens_counter), \
           NumericalStatistics(ru_tokens_counter)


araneae = Araneae()
araneae.load()
en_symbols, ru_symbols, en_tokens, ru_tokens = get_nl_sizes_statistics(araneae)
