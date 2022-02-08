from enum import Enum
from copy import deepcopy
from dataclasses import dataclass, field
from typing import *

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
    ARANEAE_BINARY_TRAIN = "araneae-binary-train"
    ARANEAE_BINARY_DEV = "araneae-binary-dev"
    ARANEAE_DATES_TRAIN = "araneae-dates-train"
    ARANEAE_DATES_DEV = "araneae-dates-dev"
    ARANEAE_FUZZY_TRAIN = "araneae-fuzzy-train"
    ARANEAE_FUZZY_DEV = "araneae-fuzzy-dev"


class QueryType(Enum):
    BINARY = "binary"
    DATETIME = "datetime"


class QuerySubtype(Enum):
    BINARY_TRUE_FALSE = "binary-true-false"
    BINARY_ANTONYMS = "binary-antonyms"
    BINARY_GENDER = "binary-gender"
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


query_type_mapping = {_t.value: _t for _t in QueryType}
query_subtype_mapping = {_t.value: _t for _t in QuerySubtype}
query_mapping = {
    QueryType.BINARY: [
        QuerySubtype.BINARY_TRUE_FALSE,
        QuerySubtype.BINARY_ANTONYMS,
        QuerySubtype.BINARY_GENDER,
        QuerySubtype.BINARY_YES_NO,
        QuerySubtype.BINARY_0_1
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
    ]
}


class Sample:
    def __init__(self):
        self.id: Optional[int] = None
        self.source: Optional[Source] = None
        self.question: Optional[str] = None
        self.query: Optional[str] = None
        self.sql: Optional[Dict] = None
        self.mentions: Optional[List[Mention]] = None
        self.specifications: Optional[Dict] = None
        self.query_toks: Optional[List] = None
        self.query_toks_no_values: Optional[List] = None

    def to_dict(self) -> Dict:
        dicted = deepcopy(self.__dict__)
        del dicted['mentions']
        del dicted['query_toks']
        del dicted['query_toks_no_values']
        for _k, _v in dicted.items():
            if isinstance(_v, Enum):
                dicted[_k] = _v.value
        for _query_type in QueryType:
            dicted[_query_type.value] = ""
            if dicted['specifications'][_query_type]:
                dicted[_query_type.value] = ', '.join([_s.value for _s in dicted['specifications'][_query_type] if _s])
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

