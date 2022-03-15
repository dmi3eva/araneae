
from araneae.wrapper import Araneae
from dataclasses import dataclass
from typing import *
from enum import Enum
import json


from configure import TOKENS_INFO_PATH


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
    table: Optional[str] = None
    column: Optional[str] = None
    value: Optional[str] = None


@dataclass
class QuestionDescription:
    db: str
    nl: Optional[str] = None


@dataclass
class QueryDescription:
    db: str
    nl: Optional[str] = None


@dataclass
class Token:
    db: Optional[Dict[str, DBDescription]] = None
    question: Optional[Dict[str, QuestionDescription]] = None
    query: Optional[Dict[str, QueryDescription]] = None


def extract_token_info(dataset: Araneae) -> Dict[str, Token]:
    pass


def save_elements_statistics(statistics, filename):
    with open(TOKENS_INFO_PATH, 'w') as f:
        json.dump(statistics, f)


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    token_info = extract_token_info(araneae)