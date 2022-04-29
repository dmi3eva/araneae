from collections import Counter
from utils.spider_connectors import *
from utils.spider_analysis import *



def get_nl_sizes_statistics(araneae) -> Tuple[NumericalStatistics, NumericalStatistics, NumericalStatistics, NumericalStatistics]:
    """
    Returns sizes of qestions in symbols and in tokens
    """

    # TODO: Turn it for excersice for students in refactoring :)

    longest_symbols_en = ""
    longest_symbols_ru = ""

    longest_tokens_en = ""
    longest_tokens_ru = ""

    english_symbols = []
    russian_symbols = []

    english_tokens = []
    russian_tokens = []

    for sample in araneae.samples.content:
        english_nl = sample.question
        russian_nl = sample.russian_question
        english_tokens = sample.russian_question_toks
        russian_tokens = sample.russian_question_toks
        english_symbols.append(len(english_nl))
        russian_symbols.append(len(russian_nl))
        english_tokens.append(len(english_tokens))
        russian_tokens.append(len(english_tokens))
        if len(english_nl) > len(longest_symbols_en):
            longest_symbols_en = english_nl
        if len(russian_nl) > len(longest_symbols_ru):
            longest_symbols_ru = russian_nl
        if len(english_tokens) > len(longest_tokens_en):
            longest_tokens_en = english_tokens
        if len(russian_tokens) > len(longest_tokens_ru):
            longest_tokens_ru = russian_tokens

    print(f"Longest english, tokens {' '.join(longest_tokens_en)} ({len(longest_tokens_en)})")
    print(f"Longest russian, tokens {' '.join(longest_tokens_ru)} ({len(longest_tokens_ru)})")

    print(f"Longest english, symbols {longest_symbols_en} ({len(longest_symbols_en)})")
    print(f"Longest russian, symbols {longest_symbols_ru} ({len(longest_symbols_en)})")

    print(f"Average english, symbols {sum(english_symbols) / len(english_symbols)}")
    print(f"Average russian, symbols {sum(russian_symbols) / len(russian_symbols)}")

    print(f"Average english, tokens {sum(english_tokens) / len(english_tokens)}")
    print(f"Average russian, tokens {sum(russian_tokens) / len(russian_tokens)}")

    en_symbols_counter = Counter(english_symbols)
    ru_symbols_counter = Counter(russian_symbols)

    en_symbols_tokens = Counter(english_symbols)
    ru_symbols_tokens = Counter(russian_symbols)

    return en_symbols_counter, ru_symbols_counter, en_symbols_tokens, ru_symbols_tokens

