from enum import Enum
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


class Sample:
    def __init__(self):
        self.question: Optional[str] = None
        self.query: Optional[str] = None
        self.sql: Optional[Dict] = None
        self.mentions: List[Mention] = None
        self.specifications: Optional[Dict] = None
        self.query_toks: Optional[List] = None
        self.query_toks_no_values: Optional[List] = None


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

