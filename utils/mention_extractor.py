import json
from enum import Enum
from dataclasses import dataclass
from typing import *


SCHEMES_PATH = "../datasets/spider/tables.json"


class Subquery(Enum):
    GROUP_BY = "group_by"


@dataclass
class Mention:
    type: Subquery
    db: Union[str, None]
    table: Union[str, None]
    column: Union[str, None]
    values: List[Union[str, None]]


def load_schemes():
    db_schemes = []
    with open(SCHEMES_PATH) as table_file:
        db_schemes = json.load(table_file)
    return {_s['db_id']: _s for _s in db_schemes}


class MentionExtractor:
    def __init__(self):
        self.schemes = load_schemes()

    def parse_col_unit(self, scheme, col_unit):
        col_id = col_unit[1]
        column_description = scheme["column_names_original"][col_id]
        column = column_description[1]
        table_id = column_description[0]
        table = scheme["table_names_original"][table_id]
        mention = Mention(
            type=Subquery.GROUP_BY,
            db=scheme["db_id"],
            column=column,
            values=None
        )
        return mention

    def extract_from_group_by(self, scheme, group_by):
        mentions = []
        for col_unit in group_by:
            mentions.append(self.parse_col_unit(scheme, col_unit))
        return mentions

    def get_mentions(self, sample: Dict) -> List[Mention]:
        mentions = []
        db = sample['db_id']
        sql = sample['sample']
        scheme = self.schemes[db]
        group_by = sql['group_by']
        mentions += [self.extract_from_group_by(scheme, group_by)]
        return mentions


if __name__ == "__main__":
    with open('../datasets/araneae/araneae.json') as table_file:
        araneae = json.load(table_file)

    extractor = MentionExtractor()
    for ind, sample in enumerate(araneae):
        question = sample['question']
        query = sample['query']
        sql = sample['sql']

        mentions = extractor.get_mentions(sample)
        a = 7






