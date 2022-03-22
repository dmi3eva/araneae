import re
import os
import json
import cProfile

from dto.sample import *
from configure import *
from utils.preprocessing.text import *


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


def get_negation_keys(words: List[str], sentence: str) -> List[str]:
    negation_keywords = {
        "no", "not", "!", "\'no", "except", "never", "without", "!=", "\'no\'", "null",
        "don't", "doesn't", "dont", "doesnt", "isn't", "isnt", "arent", "didn't", "didnt",
        "<=", ">=", "0"
    }
    processed = set([_w.lower().replace('\'', "").replace("\"", "") for _w in words])
    negations = negation_keywords.intersection(processed)
    if "<=" in sentence and "<=" not in negations:
        negations.add("<=")
    if ">=" in sentence and ">=" not in negations:
        negations.add(">=")
    return list(negations)


def contains_logic_set_phrase(sample: Sample) -> bool:
    set_phrases = [
        "or equal"
        # "or before",
        # "or later",
        # "no more",
        # "no less"
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


def db_entity_correspond_to_mention(db_entity: Dict, mention: Mention) -> bool:
    if db_entity['value'] and mention.values:
        return True
    if mention.db != db_entity["db"]:
        return False
    if mention.table != db_entity["table"]:
        return False
    if mention.column != db_entity["column"]:
        return False
    return True

def extract_tokens(sample: Sample, db_tokens: Dict, language: Language, category: str) -> Tuple[Dict, Dict]:
    db = sample.db_id
    if language is Language.EN:
        sample_tokens = sample.question_toks
        db_tokens = db_tokens[category]["en"][db]
    else:
        sample_tokens = sample.russian_question_toks
        db_tokens = db_tokens[category]["ru"][db]
    return sample_tokens, db_tokens


def contains_db_mentioned(sample: Sample, db_tokens: Dict, language: Language) -> bool:
    mentions = sample.mentions
    sample_tokens, db_tokens = extract_tokens(sample, db_tokens, language, "all")
    for question_token in sample_tokens:
        processed = db_token_process(question_token, language)
        if len(processed) < 4:  # TODO: take into frequency
            continue
        db_entities = db_tokens.get(processed, [])
        used_mentions = []
        for _db_entity in db_entities:
            for _mention in mentions:
                if db_entity_correspond_to_mention(_db_entity, _mention):
                    used_mentions.append(_mention)
        wrong_processed = ["id"]
        if len(used_mentions) == 0 and len(db_entities) > 0 and processed not in wrong_processed:
            return True
    return False


def contains_db_hetero(sample: Sample, db_tokens: Dict, language: Language) -> bool:
    sample_tokens, db_tokens = extract_tokens(sample, db_tokens, language, "all")
    for token in sample_tokens:
        if token in db_tokens.keys():
            return True
    return False


def contains_db_homo_tables(sample: Sample, db_tokens: Dict, language: Language) -> bool:
    sample_tokens, db_tokens = extract_tokens(sample, db_tokens, language, "tables")
    for token in sample_tokens:
        if token in db_tokens.keys():
            return True
    return False


def contains_db_homo_columns(sample: Sample, db_tokens: Dict, language: Language) -> bool:
    sample_tokens, db_tokens = extract_tokens(sample, db_tokens, language, "columns")
    for token in sample_tokens:
        if token in db_tokens.keys():
            return True
    return False


def contains_db_homo_values(sample: Sample, db_tokens: Dict, language: Language) -> bool:
    sample_tokens, db_tokens = extract_tokens(sample, db_tokens, language, "values")
    for token in sample_tokens:
        if token in db_tokens.keys():
            return True
    return False


if __name__ == "__main__":
    text = "who acted the role of "" Mr. Bean """
    amount = get_sentences_amount(text)
    print(amount)