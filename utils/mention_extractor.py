import json
from enum import Enum
from dataclasses import dataclass, field
from typing import *


SCHEMES_PATH = "../datasets/spider/tables.json"


class Subquery(Enum):
    SELECT = "select"
    GROUP_BY = "group_by"
    ORDER_BY = "order_by"
    HAVING = "having"
    LIMIT = "limit"


class Aggregation(Enum):
    MAX = 'max'
    MIN = 'min'
    COUNT = 'count'
    SUM = 'sum'
    AVG = 'avg'


class ORDER(Enum):
    ASC = 'max'
    DESC = 'min'


AGGREGATIONS = [None, Aggregation.MAX, Aggregation.MIN, Aggregation.COUNT, Aggregation.SUM, Aggregation.AVG]


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


def load_schemes():
    db_schemes = []
    with open(SCHEMES_PATH) as table_file:
        db_schemes = json.load(table_file)
    return {_s['db_id']: _s for _s in db_schemes}


class MentionExtractor:
    def __init__(self):
        self.schemes = load_schemes()

    def parse_col_unit(self, scheme, col_unit, type, input_details, aggregation=0, distinct=None) -> Mention:
        col_id = col_unit[1]
        column_description = scheme["column_names_original"][col_id]
        column = column_description[1]
        table_id = column_description[0]
        if table_id == -1:
            table = None
        else:
            table = scheme["table_names_original"][table_id]
        mention = Mention(
            type=type,
            db=scheme["db_id"],
            table=table,
            column=column,
            aggregation=AGGREGATIONS[aggregation],
            distinct=distinct,
            details=input_details
        )
        return mention

    def parse_val_unit(self, scheme, val_unit, type, input_details, aggregation=0, distinct=None) -> List[Mention]:
        unit_op = val_unit[0]
        col_unit_1 = val_unit[1]
        mentions = [self.parse_col_unit(scheme, col_unit_1, type, input_details, aggregation, distinct)]
        if unit_op:
            col_unit_2 = val_unit[1]
            from_col_2 = [self.parse_col_unit(scheme, col_unit_2, type, input_details + [unit_op], aggregation, distinct)]
            mentions += from_col_2
        return mentions

    def parse_condition(self, scheme, val_unit, type, input_details, aggregation=0, distinct=None) -> List[Mention]:
        mentions = []
        return mentions

    def extract_from_having(self, scheme, having, details) -> List[Mention]:
        mentions = self.parse_condition(scheme, having, Subquery.HAVING, details)
        return mentions

    def extract_from_group_by(self, scheme, group_by, details) -> List[Mention]:
        mentions = []
        for col_unit in group_by:
            mentions.append(self.parse_col_unit(scheme, col_unit, Subquery.GROUP_BY, details))
        return mentions

    def extract_from_order_by(self, scheme, order_by, details) -> List[Mention]:  # TODO
        if len(order_by) == 0:
            return []
        order = order_by[0]
        mentions = []
        for val_unit in order_by[1]:
            mentions += self.parse_val_unit(scheme, val_unit, Subquery.ORDER_BY, details + [order])
        return mentions

    def extract_from_select(self, scheme, select, details) -> List[Mention]:
        dist = select[0]
        mentions = []
        for select_unit in select[1]:
            agg = select_unit[0]
            val_unit = select_unit[1]
            mentions += self.parse_val_unit(scheme, val_unit, Subquery.SELECT, details, aggregation=agg, distinct=dist)
        return mentions

    def extract_from_limit(self, scheme, limit, details) -> List[Mention]:
        if limit is not None:
            return [Mention(type=Subquery.LIMIT, limit=int(limit))]
        return []

    def get_mentions_from_sql(self, db: str, sql: Dict, details=None) -> List[Mention]:
        mentions = []
        scheme = self.schemes[db]
        if not details:
            details = []
        mentions += self.extract_from_select(scheme, sql['select'], details)
        mentions += self.extract_from_group_by(scheme, sql['groupBy'], details)
        mentions += self.extract_from_order_by(scheme, sql['orderBy'], details)
        mentions += self.extract_from_having(scheme, sql['having'], details)
        mentions += self.extract_from_limit(scheme, sql['limit'], details)
        if sql['intersect']:
            mentions += self.get_mentions_from_sql(db, sql['intersect'], details=['intersect'])
        if sql['union']:
            mentions += self.get_mentions_from_sql(db, sql['union'], details=['union'])
        if sql['except']:
            mentions += self.get_mentions_from_sql(db, sql['except'], details=['except'])
        return mentions

    def get_mentions_from_sample(self, sample: Dict) -> List[Mention]:
        db = sample['db_id']
        sql = sample['sql']
        mentions = self.get_mentions_from_sql(db, sql)
        return mentions


if __name__ == "__main__":
    with open('../datasets/araneae/araneae.json') as table_file:
        araneae = json.load(table_file)

    extractor = MentionExtractor()
    for ind, sample in enumerate(araneae[2:]):
        question = sample['question']
        query = sample['query']
        sql = sample['sql']

        mentions = extractor.get_mentions_from_sample(sample)
        if 'group by' in query.lower():
            a = 7






