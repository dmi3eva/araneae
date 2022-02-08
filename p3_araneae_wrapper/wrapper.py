import os
import json
import pandas as pd
from copy import deepcopy
from typing import *

from utils.common import *
from utils.mention_extractor import MentionExtractor
from utils.preprocessing.custom_sql import *
from utils.preprocessing.spider.process_sql import *
from dto.sample import *

COLUMN_TYPES = ["binary", "dates"]

SPIDER_PATH = "../resources/datasets/spider"
QUERY_TYPES_PATH = "../resources/query_types"


class Araneae:
    def __init__(self):
        self.samples = []
        self.column_types = {}
        self.load_column_types()
        self.mention_extractor = MentionExtractor()

    def load_column_types(self):
        for _column_type in COLUMN_TYPES:
            path = os.path.join(QUERY_TYPES_PATH, f"{_column_type}.json")
            self.column_types[_column_type] = {}
            with open(path) as column_file:
                self.column_types[_column_type] = json.load(column_file)

    def load_spider(self):
        pass

    def load(self):
        pass

    def save(self):
        pass

    def create_sample_from_json(self, sample_json) -> Sample:
        generated_sample = Sample()
        generated_sample.question = sample_json.get('question', None)
        generated_sample.query = sample_json.get('query', None)
        generated_sample.sql = sample_json.get('question', None)
        generated_sample.query_toks = sample_json.get('query_toks', None)
        generated_sample.query_toks_no_values = sample_json.get('query_toks_no_values', None)
        generated_sample.mentions = self.mention_extractor.get_mentions_from_sample(sample_json)
        generated_sample.specifications = self.extract_specifications()

    def extract_specifications(self):
        pass


class AraneaeWrapper:
    def __init__(self, samples_path, tables_path, db_path):
        self.samples = []
        self.db_path = db_path
        with open(samples_path) as sample_file:
            self.samples = json.load(sample_file)
        with open(tables_path) as tables_file:
            self.tables = json.load(tables_file)
        for _sample in self.samples:
            _sample['sql_units'] = get_units_from_sample(_sample)
        self.samples = [self.augment_sample(_sample) for _sample in self.samples]

    def augment_sample(self, sample):
        if 'description' not in sample.keys():
            sample['description'] = {}
        if 'tags' not in sample.keys():
            sample['tags'] = []
        if 'question_toks' not in sample.keys():
            sample['question_toks'] = tokenize(sample['question'])

        if 'sql' not in sample.keys():
            db_id = sample['db_id']
            db = get_schema(f"{self.db_path}/{db_id}/{db_id}.sqlite")
            schema = Schema(db)
            sql_dict = get_sql(schema, sample['query'])
            sample['sql'] = sql_dict
            query_no_value = sample['query']
            for _value in unfold_list(sql_dict['where']):
                if str(_value) in query_no_value:
                    query_no_value = query_no_value.replace(str(_value), 'value')
            sample['question_toks_no_value'] = tokenize(query_no_value)

        augmented_sample = deepcopy(sample)
        augmented_sample = self.add_nl_tag(augmented_sample)
        augmented_sample = self.add_binary_tag(augmented_sample)
        augmented_sample = self.add_dates_tag(augmented_sample)

        return augmented_sample

    def add_nl_tag(self, sample):
        SHORT_THRESHOLD = 13
        LONG_THRESHOLD = 17
        if 'NL-length' in sample['description']:
            return sample
        tag = None
        augmented_sample = deepcopy(sample)
        request_len = len(sample['question_toks'])
        if request_len <= SHORT_THRESHOLD:
            tag = "NL-short"
        elif request_len <= LONG_THRESHOLD:
            tag = "NL-avg"
        else:
            tag = "NL-long"
        augmented_sample['tags'].append(tag)
        augmented_sample['description']['NL-length'] = tag
        return augmented_sample

    def add_binary_tag(self, sample):
        augmented_sample = deepcopy(sample)
        for _unit in sample['sql_units']:
            db_id = _unit['db_id']
            table = _unit['table']
            column = _unit['column']
            if column in binary_values.get(db_id, {}).get(table, {}).keys():
                augmented_sample['tags'].append('binary-values')
                augmented_sample['description']['binary'] = [binary_values[db_id][table][column]]
            else:
                augmented_sample['description']['binary'] = ['not-binary']
        return augmented_sample

    def add_dates_tag(self, sample):
        augmented_sample = deepcopy(sample)
        for _unit in sample['sql_units']:
            db_id = _unit['db_id']
            table = _unit['table']
            column = _unit['column']
            if column in dates_values.get(db_id, {}).get(table, {}).keys():
                augmented_sample['tags'].append('datetimes')
                augmented_sample['description']['dates'] = dates_values[db_id][table][column]
            else:
                augmented_sample['description']['dates'] = ['not-date']
        return augmented_sample

    def get_samples_with_tag(self, tag):
        samples_with_tag = [_s for _s in self.samples if tag in _s['tags']]
        return samples_with_tag

    def add_sample(self, nl, db_id, sql, source, tag=None, description: Tuple[str, str] = (None, None)):
        new_sample = {
            'db_id': db_id,
            'question': nl,
            'source': source,
            'query': preprocess_SQL(sql),
            'tags': [],
            'description': {}
        }
        if tag:
            new_sample['tags'].append(tag)
        if description[0] and description[1]:
            new_sample['description'][description[0]] = description[1]
        new_sample = self.augment_sample(new_sample)
        self.samples.append(new_sample)

    def add_samples_from_csv(self, file_path, tag=None, description: Tuple[str, str] = (None, None)):
        new_samples = pd.read_csv(file_path)
        for ind, row in new_samples.iterrows():
            self.add_sample(row['nl'], row['db_id'], row['sql'], file_path, tag=tag, description=description)

    def save_in_json(self, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(self.samples, json_file)