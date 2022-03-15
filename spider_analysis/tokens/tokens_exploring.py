
from araneae.wrapper import Araneae
from dto.sample import *
from dataclasses import dataclass
from typing import *
from enum import Enum
import json


from configure import *


class Entity(Enum):
    DB = 0
    TABLE = 1
    COLUMN = 2
    VALUE = 3
    AGG = 4


@dataclass
class DBDescription:
    type: Entity
    db: str
    id: int
    table: Optional[str] = None
    column: Optional[str] = None
    value: Optional[str] = None


@dataclass
class QuestionDescription:
    db: str
    id: int
    nl: Optional[str] = None


@dataclass
class QueryDescription:
    db: str
    id: int
    nl: Optional[str] = None


@dataclass
class Token:
    db: Optional[Dict[str, DBDescription]] = None
    question: Optional[Dict[str, QuestionDescription]] = None
    query: Optional[Dict[str, QueryDescription]] = None


def token_process(token: str, language: Language) -> str:
    processed = token.lower()
    return processed

def extract_tokens_info(dataset: Araneae, language: Language):
    info = dict()
    info = extract_question_info(info, dataset, language)
    # info = extract_query_info(info, dataset, language)
    # info = extract_db_info(info, dataset, language)
    return info


def extract_question_info(info: Dict[str, Token], dataset: Araneae, language: Language) -> Dict[str, Token]:
    for sample in dataset.samples.content:
        tokens = []
        nl = ""
        if language is Language.EN:
            tokens = sample.question_toks
            nl = sample.question
        if language is Language.RU:
            tokens = sample.russian_question_toks
            nl = sample.russian_question
        for _token in tokens:
            info = get_question_token(info, token_process(_token, language), sample.db_id, nl, sample.id)
    return info


def extract_query_info(info: Dict[str, Token], dataset: Araneae, language: Language) -> Dict[str, Token]:
    for sample in dataset.samples.content:
        mentions = sample.mentions
        if language is Language.EN:
            nl = sample.query
        if language is Language.RU:
            nl = sample.russian_query
        for _mention in mentions:
            info = get_query_token(info, _mention, sample.db_id, nl, sample.id)
    return info


def get_question_token(info: Dict[str, Token], token: str, db: str, nl: str, id: int) -> Dict[str, Token]:
    if len(token) < MIN_TOKEN_LENGTH:
        return info
    info[token] = info.get(token, Token())
    if not info[token].question:
        info[token].question = {}
    db_info = info[token].question.get(db, [])
    db_info.append(
        QuestionDescription(db=db, nl=nl, id=id)
    )
    info[token].question[db] = db_info
    return info


def get_query_token(info: Dict[str, Token], mention: Mention, db: str, nl: str, id: int) -> Dict[str, Token]:
    tokens = extract_token_from_mentions(mention)
    for _token in tokens:
        info[_token] = info.get(_token, Token())
        if not info[_token].question:
            info[_token].question = {}
        db_info = info[_token].question.get(db, [])
        db_info.append(
            QueryDescription(db=db, nl=nl, id=id)
        )
        info[_token].question[db] = db_info
    return info


def extract_token_from_mentions(mention: Mention) -> List[str]:
    if mention.values:
        return mention.values  # Short tokens also remains
    token = ""
    if mention.column:
        token = mention.column
    elif mention.table:
        token = mention.table
    if len(token) > MIN_TOKEN_LENGTH:
        tokens = [token]
    else:
        tokens = []
    return tokens


def info_to_dict(statistics: Dict) -> Dict:
    info = {}
    for token_name, token in statistics.items():
        a = 7
        info[token_name] = {
            "db": {},
            "question": {},
            "query": {}
        }
        if token.question:
            info[token_name]["question"] = {
                _db: [_q.__dict__ for _q in _questions]
                for _db, _questions in token.question.items()
            }
        if token.query:
            info[token_name]["query"] = {
                _db: [_q.__dict__ for _q in _queries]
                for _db, _queries in token.question.items()
            }
        if token.db:
            info[token_name]["db"] = {
                _db: [_d.__dict__ for _d in _dbs]
                for _db, _dbs in token.question.items()
            }
    return info


def save_tokens_info(statistics, filename) -> NoReturn:
    tokens_info = info_to_dict(statistics)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tokens_info, f, ensure_ascii=False)


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()

    en_tokens = extract_tokens_info(araneae, Language.EN)
    save_tokens_info(en_tokens, TOKENS_EN_PATH)

    ru_tokens = extract_tokens_info(araneae, Language.RU)
    save_tokens_info(ru_tokens, TOKENS_RU_PATH)