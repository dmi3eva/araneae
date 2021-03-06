import json
import pandas as pd

from enum import Enum
from copy import deepcopy
from dataclasses import dataclass, field
from typing import *


class Language(Enum):
    RU = 0
    EN = 1


class Detail(Enum):
    MULTI_CONDITIONS = "multi-conditions"
    ORDER_ASC = "order-asc"
    ORDER_DESC = "order-desc"
    MULTI_OPERATIONS = "multi-operations"
    FROM_VALUE = "from-value"
    SUB_SQL = "sub_sql"


class Subquery(Enum):
    SELECT = "select"
    FROM = "from"
    GROUP_BY = "group_by"
    ORDER_BY = "order_by"
    HAVING = "having"
    WHERE = "where"
    LIMIT = "limit"


class Aggregation(Enum):
    MAX = 'max'
    MIN = 'min'
    COUNT = 'count'
    SUM = 'sum'
    AVG = 'avg'


class Order(Enum):
    ASC = 'max'
    DESC = 'min'


class Source(Enum):
    SPIDER_DEV = "spider-dev"
    SPIDER_TRAIN = "spider-train"
    SPIDER_TRAIN_OTHERS = "spider-train-others"
    ADDITION = "addition"
    ARANEAE_BINARY_TRAIN = "araneae-binary-train"
    ARANEAE_BINARY_DEV = "araneae-binary-dev"
    ARANEAE_DATES_TRAIN = "araneae-dates-train"
    ARANEAE_DATES_DEV = "araneae-dates-dev"
    ARANEAE_FUZZY_TRAIN = "araneae-fuzzy-train"
    ARANEAE_FUZZY_DEV = "araneae-fuzzy-dev"


class TrainDevType(Enum):
    TRAIN = "train"
    DEV = "dev"


class QueryType(Enum):
    TWO = "two"
    DATETIME = "datetime"
    SIMPLICITY = "simplicity"
    JOIN = "join"
    SELECT = "select"
    LOGIC = "logic"
    NEGATION = "negation"
    NL = "nl"
    DB = "db"
    SQL = "sql"
    WHERE = "where"
    GROUP_BY = "group_by"
    ORDER_BY = "order_by"
    NEW = "new"


class QuerySubtype(Enum):
    WITH_VALUES = "with_values"
    WITHOUT_VALUES = "without_values"
    BINARY_TRUE_FALSE = "binary-true-false"
    TWO_ANTONYMS = "binary-antonyms"
    TWO_GENDER = "binary-gender"
    BINARY_YES_NO = "binary-yes-no"
    BINARY_0_1 = "binary-0-1"
    DATE = "date"
    TIME = "time"
    TIME_HOURS = "time-hours"
    DATE_PERIOD = "date-period"
    DATE_BIRTH = "date-birth"
    DATETIME_BIRTH = "datetime-birth"
    DATE_WEEKDAY = "date-weekday"
    DATETIME_START = "datetime-start"
    DATETIME_END = "datetime-end"
    DATETIME = "datetime"
    TIME_DURATION = "time-duration"
    TIME_PERIOD = "time-period"
    DATETIME_PLANNED = "datetime-planned"
    DATETIME_ACTUAL = "datetime-actual"
    DATETIME_ORDER = "datetime-order"
    SIMPLE = "simple"
    EXTRA_SIMPLE = "extra-simple"
    SINGLE_JOIN = "single-join"
    MULTI_JOIN = "multi-join"
    MULTI_SELECT = "multi-select"
    HETERO_AGG = "hetero-agg"
    MONO_AGG = "mono-agg"
    NESTED = "nested"
    LOGIC_NL_ALL = "logic-nl-all"
    LOGIC_SQL_ALL = "logic-sql-all"
    LOGIC_NL_AND_OR_OR = "logic-nl-and-or-or"
    LOGIC_NL_AND_AND_OR = "logic-nl-and-and-or"
    LOGIC_SQL_AND_OR = "logic-sql-and-or"
    LOGIC_VS = "logic-vs"
    LOGIC_SET_PHRASE = "logic-set-phrase"
    NEGATION_NL = "negation-nl"
    NEGATION_SQL = "negation-sql"
    NEGATION_SET_PHRASE =  "negation-set-phrase"
    NEGATION_NEVER = "negation-never"
    NEGATION_EXCEPT = "negation-except"
    NEGATION_NOT_EQUAL = "negation-not-equal"
    NEGATION_NOT_ONLY = "negation-not-only"
    NEGATION_COMMON_KNOWLEDGE = "negation-common-knowledge"
    NEGATION_NEITHER_NOR = "negation-neither-nor"
    NEGATION_IGNORING = "negation-ignoring"
    NEGATION_OTHER_THAN = "negation-other-than"
    NEGATION_OUTSIDE = "negation-outside"
    NEGATION_ANY_ALL = "negation-any-all"
    NEGATION_NULL = "negation-null"
    NL_SEVERAL_SENTENCES = "nl-several-sentences"
    NL_LONG_SQL_SHORT = "nl-long-sql-short"
    NL_SHORT_SQL_LONG = "nl-short-sql-long"
    NL_LONG = "nl-long"
    DB_EN_MENTIONED_BUT_NOT_USED = "db-en-mentioned-but-not-used"
    DB_EN_HETERO_AMBIGUITY = "db-en-hetero-ambiguity"
    DB_EN_TABLES_AMBIGUITY = "db-en-tables-ambiguity"
    DB_EN_COLUMNS_AMBIGUITY = "db-en-columns-ambiguity"
    DB_EN_VALUES_AMBIGUITY = "db-en-values-ambiguity"
    DB_RU_MENTIONED_BUT_NOT_USED = "db-ru-mentioned-but-not-used"
    DB_RU_HETERO_AMBIGUITY = "db-ru-hetero-ambiguity"
    DB_RU_TABLES_AMBIGUITY = "db-ru-tables-ambiguity"
    DB_RU_COLUMNS_AMBIGUITY = "db-ru-columns-ambiguity"
    DB_RU_VALUES_AMBIGUITY = "db-ru-values-ambiguity"
    SQL_LIKE = "sql-like"
    SQL_LIMIT = "sql-limit"
    SQL_CAST = "sql-cast"
    SQL_HAVING = "sql-having"
    SQL_MULTI_WHERE = "sql-multi-where"
    SQL_BETWEEN = "sql-between"
    SQL_COMPARE = "sql-compare"
    SQL_NULL = "sql-null"
    SQL_EXCEPT = "sql-except"
    SQL_DISCTINCT = "sql-distinct"
    SQL_EXISTS = "sql-exists"
    WHERE_MONO = "where-mono"
    WHERE_MULTI = "where-multi"
    GROUP_BY_EXISTS = "group-by-exists"
    GROUP_BY_COUNT = "group-by-count"
    ORDER_BY_EXISTS = "order-by-exists"
    ORDER_BY_COUNT = "order-by-count"
    NEW_ALL = "new"
    NEW_FUZZY = "fuzzy"
    NEW_LONG = "long"
    NEW_EMPTY = "empty"
    NEW_BINARY = "new_binary"
    NEW_DATES = "new_dates"
    OLD_LONG = "old_long"
    DATES_WITH_NEW = "dates-all"
    TWO_WITHOUT_VALUES = "two-without-values"
    JUST_BINARY = "just-binary"
    JUST_BINARY_OLD = "just-binary-old"
    AGG_IN_COLUMN = "aggregation-in-column"


query_type_mapping = {_t.value: _t for _t in QueryType}
query_subtype_mapping = {_t.value: _t for _t in QuerySubtype}
query_mapping = {
    QueryType.TWO: [
        QuerySubtype.BINARY_TRUE_FALSE,
        QuerySubtype.TWO_ANTONYMS,
        QuerySubtype.TWO_GENDER,
        QuerySubtype.BINARY_YES_NO,
        QuerySubtype.BINARY_0_1,
        QuerySubtype.TWO_WITHOUT_VALUES,
        QuerySubtype.JUST_BINARY,
        QuerySubtype.JUST_BINARY_OLD
    ],
    QueryType.DATETIME: [
        QuerySubtype.DATE,
        QuerySubtype.TIME,
        QuerySubtype.TIME_HOURS,
        QuerySubtype.DATE_PERIOD,
        QuerySubtype.DATE_BIRTH,
        QuerySubtype.DATETIME_BIRTH,
        QuerySubtype.DATE_WEEKDAY,
        QuerySubtype.DATETIME_START,
        QuerySubtype.DATETIME_END,
        QuerySubtype.DATETIME,
        QuerySubtype.TIME_DURATION,
        QuerySubtype.TIME_PERIOD,
        QuerySubtype.DATETIME_PLANNED,
        QuerySubtype.DATETIME_ACTUAL,
        QuerySubtype.DATETIME_ORDER,
    ],
    QueryType.SELECT: [
        QuerySubtype.MULTI_SELECT,
        QuerySubtype.HETERO_AGG,
        QuerySubtype.MONO_AGG,
        QuerySubtype.NESTED
    ],
    QueryType.NL: [
        QuerySubtype.NL_SEVERAL_SENTENCES,
        QuerySubtype.NL_LONG_SQL_SHORT,
        QuerySubtype.NL_SHORT_SQL_LONG,
        QuerySubtype.NL_LONG
    ],
    QueryType.LOGIC: [
        QuerySubtype.LOGIC_NL_ALL,
        QuerySubtype.LOGIC_SQL_ALL,
        QuerySubtype.LOGIC_NL_AND_OR_OR,
        QuerySubtype.LOGIC_NL_AND_AND_OR,
        QuerySubtype.LOGIC_SQL_AND_OR,
        QuerySubtype.LOGIC_VS,
        QuerySubtype.LOGIC_SET_PHRASE
    ],
    QueryType.NEGATION: [
        QuerySubtype.NEGATION_NL,
        QuerySubtype.NEGATION_SQL,
        QuerySubtype.NEGATION_SET_PHRASE,
        QuerySubtype.NEGATION_NEVER,
        QuerySubtype.NEGATION_EXCEPT,
        QuerySubtype.NEGATION_NOT_EQUAL,
        QuerySubtype.NEGATION_NOT_ONLY,
        QuerySubtype.NEGATION_COMMON_KNOWLEDGE,
        QuerySubtype.NEGATION_NEITHER_NOR,
        QuerySubtype.NEGATION_IGNORING,
        QuerySubtype.NEGATION_OTHER_THAN,
        QuerySubtype.NEGATION_OUTSIDE,
        QuerySubtype.NEGATION_ANY_ALL,
        QuerySubtype.NEGATION_NULL
    ],
    QueryType.DB: [
        QuerySubtype.DB_EN_MENTIONED_BUT_NOT_USED,
        QuerySubtype.DB_EN_HETERO_AMBIGUITY,
        QuerySubtype.DB_EN_TABLES_AMBIGUITY,
        QuerySubtype.DB_EN_COLUMNS_AMBIGUITY,
        QuerySubtype.DB_EN_VALUES_AMBIGUITY,
        QuerySubtype.DB_RU_MENTIONED_BUT_NOT_USED,
        QuerySubtype.DB_RU_HETERO_AMBIGUITY,
        QuerySubtype.DB_RU_TABLES_AMBIGUITY,
        QuerySubtype.DB_RU_COLUMNS_AMBIGUITY,
        QuerySubtype.DB_RU_VALUES_AMBIGUITY
    ],
    QueryType.SQL: [
        QuerySubtype.SQL_LIKE,
        QuerySubtype.SQL_LIMIT,
        QuerySubtype.SQL_CAST,
        QuerySubtype.SQL_HAVING,
        QuerySubtype.SQL_MULTI_WHERE,
        QuerySubtype.SQL_BETWEEN,
        QuerySubtype.SQL_COMPARE,
        QuerySubtype.SQL_NULL,
        QuerySubtype.SQL_EXCEPT,
        QuerySubtype.SQL_DISCTINCT,
        QuerySubtype.SQL_EXISTS
    ],
    QueryType.WHERE: [
        QuerySubtype.WHERE_MONO,
        QuerySubtype.WHERE_MULTI
    ],
    QueryType.GROUP_BY: [
        QuerySubtype.GROUP_BY_EXISTS,
        QuerySubtype.GROUP_BY_COUNT
    ],
    QueryType.ORDER_BY: [
        QuerySubtype.ORDER_BY_EXISTS,
        QuerySubtype.ORDER_BY_COUNT
    ],
    QueryType.NEW: [
        QuerySubtype.NEW_ALL,
        QuerySubtype.NEW_FUZZY,
        QuerySubtype.NEW_LONG,
        QuerySubtype.NEW_EMPTY,
        QuerySubtype.NEW_BINARY,
        QuerySubtype.NEW_DATES,
        QuerySubtype.AGG_IN_COLUMN
    ]
}


@dataclass
class Triple:
    db: str
    table: str
    column: str


class Sample:
    def __init__(self):
        self.id: Optional[str] = None
        self.db_id: Optional[str] = None
        self.source: Optional[Source] = None
        self.type: Optional[TrainDevType] = None
        self.question: Optional[str] = None
        self.query: Optional[str] = None
        self.sql: Optional[Dict] = None
        self.mentions: Optional[List[Mention]] = None
        self.russian_mentions: Optional[List[Mention]] = None
        self.russian_mentions: Optional[List[Mention]] = None
        self.specifications: Optional[Dict] = None
        self.question_toks: Optional[List] = None
        self.query_toks: Optional[List] = None
        self.query_toks_no_values: Optional[List] = None
        self.russian_question: Optional[str] = None
        self.russian_query: Optional[str] = None
        self.russian_query_toks: Optional[str] = None
        self.russian_question_toks: Optional[List] = None
        self.russian_query_toks_no_values: Optional[List] = None
        self.sql: Optional[Dict] = None
        self.russian_sql: Optional[Dict] = None

    def to_json(self) -> Dict:
        jsoned = {
            'id': self.id,
            'db_id': self.db_id,
            'source': self.source.value,
            'type': self.type.value,
            'query': {
                'en': self.query,
                'ru': self.russian_query
            },
            'question': {
                'en': self.question,
                'ru': self.russian_question
            },
            'sql': {
                'en': self.sql,
                'ru': self.russian_sql
            },
            'question_toks': {
                'en': self.question_toks,
                'ru': self.russian_question_toks
            },
            'query_toks': {
                'en': self.query_toks,
                'ru': self.russian_query_toks
            },
            'query_toks_no_values':{
                'en': self.query_toks_no_values,
                'ru': self.russian_query_toks_no_values
            }
        }
        return jsoned

    def to_dict(self) -> Dict:
        dicted = deepcopy(self.__dict__)
        del dicted['mentions']
        del dicted['russian_mentions']
        del dicted['query_toks']
        del dicted['query_toks_no_values']
        del dicted['question_toks']
        del dicted['russian_query_toks']
        del dicted['russian_query_toks_no_values']
        del dicted['russian_question_toks']

        for _k, _v in dicted.items():
            if isinstance(_v, Enum):
                dicted[_k] = _v.value
        for _query_type in QueryType:
            dicted[_query_type.value] = ""
            dicted[f"{_query_type.value}-with-values"] = False
            if not _query_type in dicted['specifications'].keys() or not dicted['specifications'][_query_type]:
                continue
            dicted[_query_type.value] = ', '.join([_s.value for _s in dicted['specifications'][_query_type] if _s])
            if QuerySubtype.WITH_VALUES in dicted['specifications'][_query_type]:
                dicted[f"{_query_type.value}-with-values"] = True
        del dicted['specifications']
        return dicted


@dataclass
class Mention:
    type: Subquery
    db: Optional[str] = None
    table: Optional[str] = None
    column: Optional[str] = None
    values: Optional[List[str]] = None
    aggregation: Optional[List[str]] = None
    distinct: bool = False
    limit: Optional[int] = None
    details: List[str] = field(default_factory=lambda: [])
    db_tokens: Optional[List[str]] = None
    query_text: Optional[str] = None
    query_mask: Optional[List[bool]] = None


class SamplesCollection:
    def __init__(self):
        self.content: List[Sample] = []

    def add(self, new_sample: Sample):
        self.content.append(new_sample)

    def save_in_csv(self, csv_path, static_content: Dict = None):
        if not static_content:
            static_content = {}
        data = []
        for _sample in self.content:
            row = _sample.to_dict()
            row.update(static_content)
            data.append(row)
        df = pd.DataFrame(data=data)
        df.to_csv(csv_path, encoding='utf-8')

    def save_in_json(self, json_path):
        data = []
        for _sample in self.content:
            row = _sample.to_dict()
            data.append(row)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def split_by_subtypes(self, query_type: QueryType, tgt_path: str):
        data = []
        for _sample in self.content:
            row = {
                'id': _sample.id,
                'question': _sample.question,
                'query': _sample.query
            }
            for _subtype in query_mapping[query_type]:
                if not _sample.specifications[query_type]:
                    continue
                if query_type not in _sample.specifications.keys():
                    continue
                if _subtype in _sample.specifications[query_type]:
                    row[_subtype.name] = 1
                else:
                    row[_subtype.name] = ""
            data.append(row)
        df = pd.DataFrame(data=data)
        df.to_csv(tgt_path, encoding='utf-8')