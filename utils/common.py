import re
import os
import cProfile

from dto.sample import *
from configure import *


def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = os.path.join(PROF_PATH, func.__name__ + '.prof')
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper


def if_extra_simple(sample: Sample) -> bool:
    """"
    Checking if query = SELECT <SOLE_COLUMN> FROM <SOLE_TABLE>
    """
    mentions = sample.mentions
    selects = [_m for _m in mentions if _m.type is Subquery.SELECT]
    froms = [_m for _m in mentions if _m.type is Subquery.FROM]
    if len(mentions) == 2 and len(selects) == 1 and len(froms) == 1:
        return True
    return False


def if_simple(sample: Sample) -> bool:
    """"
    Checking if query = SELECT <SOLE_COLUMN> FROM <SOLE_TABLE> WHERE <SOLE_CONDITION>
    """
    mentions = sample.mentions
    selects = [_m for _m in mentions if _m.type is Subquery.SELECT]
    froms = [_m for _m in mentions if _m.type is Subquery.FROM]
    wheres = [_m for _m in mentions if _m.type is Subquery.WHERE]
    if len(mentions) == 3 and len(selects) == 1 and len(froms) == 1 and len(wheres) == 1:
        return True
    return False


def if_single_join(sample: Sample) -> bool:
    joins = [_t for _t in sample.query_toks if _t.lower() == 'join']
    if len(joins) == 1:
        return True
    return False


def if_multi_join(sample: Sample) -> bool:
    joins = [_t for _t in sample.query_toks if _t.lower() == 'join']
    if len(joins) > 1:
        return True
    return False


def if_multi_select(sample: Sample) -> bool:
    mentions = sample.mentions
    selects = [_m for _m in mentions if _m.type is Subquery.SELECT]
    if len(selects) > 1:
        return True
    return False


def if_hetero_agg(sample: Sample) -> bool:
    mentions = sample.mentions
    selects = [_m for _m in mentions if _m.type is Subquery.SELECT]
    columns = [_m.column for _m in selects]
    if len(columns) != len(set(columns)):
        return True
    return False


def if_mono_agg(sample: Sample) -> bool:
    mentions = sample.mentions
    selects = [_m for _m in mentions if _m.type is Subquery.SELECT]
    aggs = [_m.aggregation for _m in selects if _m.aggregation]
    if len(aggs) != len(set(aggs)):
        return True
    return False


def get_logic_keys_from_sql(words: List[str]) -> List[str]:
    keywords = {"and", "or", "not", "all", "any", "some", "in", "between", "exists", "in", "like", "union", "intersect"}
    logic_words = [_w.lower() for _w in words if _w.lower() in keywords]
    return logic_words


def get_logic_keys_from_nl(words: List[str]) -> List[str]:
    keywords = {"and", "or", "not", "all", "any", "some", "between", "exists",
                "и", "или", "не", "все", "некоторые", "хотя", "между", "существует", "любой"}
    logic_words = []
    if words:
        logic_words = [_w.lower() for _w in words if _w.lower() in keywords]
    return logic_words


def get_negation_keys(words: List[str]) -> List[str]:
    negations = {"no", "not"}
    processed = set([_w.lower() for _w in words])
    return list(negations.intersection(processed))


def contains_logic_set_phrase(sample: Sample) -> bool:
    set_phrases = [
        "or equal"
    ]
    processed_question = sample.question.lower()
    for _phrase in set_phrases:
        if _phrase in processed_question:
            return True
    return False


def punctuation_processing(text: str) -> str:
    text = text.lower()
    text = re.sub("[!?.]+", '.', text)
    text = re.sub("mr.", '', text)
    text = re.sub("ph.d.", '', text)
    text = re.sub("i.e.", '', text)
    text = re.sub(".\d", '', text)
    text = re.sub(" \w.", '', text)
    return text


def get_sentences_amount(text: str) -> int:
    processed = punctuation_processing(text)
    sentences = processed.split('.')
    sentences = list(filter(lambda x: len(x) > 0, sentences))
    sentences_amount = len(sentences)
    return sentences_amount


if __name__ == "__main__":
    text = "who acted the role of "" Mr. Bean """
    amount = get_sentences_amount(text)
    print(amount)