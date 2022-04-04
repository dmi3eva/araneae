from typing import *
from enum import Enum
from dataclasses import dataclass


class Status(Enum):
    READY = 0
    IN_PROGRESS_FLUENCY_SOURCE = 1
    IN_PROGRESS_FLUENCY_SUBSTITUTION = 2
    IN_PROGRESS_EQUIVALENT = 3
    IN_PROGRESS_SQL = 4
    ERROR_DESCRIBING_FLUENCY_SOURCE = 5
    ERROR_DESCRIBING_FLUENCY_SUBSTITUTION = 6
    ERROR_DESCRIBING_EQUIVALENT = 7
    ERROR_DESCRIBING_SQL = 8
    LAST = 9
    CHOOSING_TABLE = 10
    VIEW_TABLE = 11
    INFO_READING = 12


class State(Enum):
    SAMPLE = 0
    TABLES = 1
    VIEW = 2
    INFO = 3
    ERROR = 4


@dataclass
class BotSample:
    id: Optional[int] = None
    db: Optional[str] = None
    source_nl: Optional[str] = None
    source_sql: Optional[str] = None
    substituted_nl: Optional[str] = None
    substituted_sql: Optional[str] = None
    paraphrased_nl: Optional[str] = None
    result: Optional[str] = None
    ok_fluency_source: bool = True
    ok_fluency_substitution: bool = True
    ok_equivalent: bool = True
    ok_sql: bool = True