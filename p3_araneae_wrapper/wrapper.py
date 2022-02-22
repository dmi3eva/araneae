import os
import json
import pandas as pd
from copy import deepcopy
from typing import *

from utils.common import *
from utils.mention_extractor import MentionExtractor
# from utils.preprocessing.custom_sql import *
# from utils.preprocessing.spider.process_sql import *
from dto.sample import *


SPIDER_PATH = "../resources/datasets/spider"
QUERY_TYPES_PATH = "../resources/query_types"


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
        with open(json_path, 'w') as f:
            json.dump(data, f)


class Araneae:
    def __init__(self):
        self.samples: SamplesCollection = SamplesCollection()
        self.column_types = {}
        self.load_column_types()
        self.mention_extractor = MentionExtractor()
        self.EXTRACTION_FUNCTIONS = {
            QueryType.BINARY: lambda s: self._specifications_from_mentions(QueryType.BINARY, s),
            QueryType.DATETIME: lambda s: self._specifications_from_mentions(QueryType.DATETIME, s)
        }

    def load_column_types(self):
        for _column_type in QueryType:
            path = os.path.join(QUERY_TYPES_PATH, f"{_column_type.value}.json")
            self.column_types[_column_type] = {}
            with open(path) as column_file:
                self.column_types[_column_type] = json.load(column_file)

    def load_from_json(self, filepath: str, source: Source):
        with open(filepath) as json_file:
            json_samples = json.load(json_file)
        for _json_sample in json_samples:
            sample = self.create_sample_from_json(_json_sample, source)
            self.samples.content.append(sample)

    def load_from_csv(self, filepath: str, source: Source):
        pass

    def load_spider(self):
        dev_path = os.path.join(SPIDER_PATH, 'dev.json')
        train_spider_path = os.path.join(SPIDER_PATH, 'train_spider.json')
        train_others_path = os.path.join(SPIDER_PATH, 'train_others.json')
        self.load_from_json(dev_path, Source.SPIDER_DEV)
        self.load_from_json(train_spider_path, Source.SPIDER_TRAIN)
        self.load_from_json(train_others_path, Source.SPIDER_TRAIN_OTHERS)

    def load(self):
        pass

    def save(self):
        pass

    def create_sample_from_json(self, sample_json: Dict, source: Source) -> Sample:
        generated_sample = Sample()
        generated_sample.id = len(self.samples.content)
        generated_sample.db_id = sample_json.get('db_id', None)
        generated_sample.source = source
        generated_sample.question = sample_json.get('question', None)
        generated_sample.query = sample_json.get('query', None)
        generated_sample.sql = sample_json.get('question', None)
        generated_sample.query_toks = sample_json.get('query_toks', None)
        generated_sample.query_toks_no_values = sample_json.get('query_toks_no_values', None)
        generated_sample.mentions = self.mention_extractor.get_mentions_from_sample(sample_json)
        generated_sample.specifications = self.extract_specifications(generated_sample)
        return generated_sample

    def extract_specifications(self, sample: Sample) -> Dict:
        specifications = {}
        for _query_type in QueryType:
            specifications[_query_type] = self.EXTRACTION_FUNCTIONS[_query_type](sample)
        return specifications

    def _specifications_from_mentions(self, query_type: QueryType, sample: Sample) -> Optional[List[QuerySubtype]]:
        specifications = None
        values = self.column_types[query_type]
        for _mention in sample.mentions:
            if not _mention.db or not _mention.table or not _mention.column:
                continue
            column_type_value = values.get(_mention.db, {}).get(_mention.table, {}).get(_mention.column, None)
            if not column_type_value:
                continue
            subtype = query_subtype_mapping[column_type_value["type"]]
            if not specifications:
                specifications = []
            specifications += [subtype]
            if _mention.values:
                specifications += [QuerySubtype.WITH_VALUES]
        if specifications:
            specifications = list(set(specifications))
        return specifications

    def find_all_with_type(self, type_for_search: QueryType) -> SamplesCollection:
        search_result = SamplesCollection()
        for _sample in self.samples.content:
            subtypes = _sample.specifications[type_for_search]
            if subtypes:
                search_result.add(_sample)
        return search_result


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load_spider()
    binary = araneae.find_all_with_type(QueryType.BINARY)
    datetimes = araneae.find_all_with_type(QueryType.DATETIME)
    binary.save_in_csv('../resources/results/with_binary.csv')
    datetimes.save_in_csv('../resources/results/with_datetimes.csv')
    binary.save_in_json('../resources/results/with_binary.json')
    datetimes.save_in_json('../resources/results/with_datetimes.json')
    a = 7

