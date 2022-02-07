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

