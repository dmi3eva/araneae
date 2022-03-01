import os
import json
import dill as pickle
import pandas as pd
from configure import *
from copy import deepcopy
from typing import *

from utils.common import *
from utils.mention_extractor import MentionExtractor
# from utils.preprocessing.custom_sql import *
# from utils.preprocessing.spider.process_sql import *
from dto.sample import *


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


class Araneae:
    def __init__(self):
        self.samples: SamplesCollection = SamplesCollection()
        self.column_types = {}
        self.load_column_types()
        self.mention_extractor = MentionExtractor()
        self.start_indices = None
        self.EXTRACTION_FUNCTIONS = {
            QueryType.BINARY: lambda sample: self._specifications_from_mentions(QueryType.BINARY, sample),
            QueryType.DATETIME: lambda sample: self._specifications_from_mentions(QueryType.DATETIME, sample),
            QueryType.SIMPLICITY: lambda sample: self._specifications_simplicity(sample),
            QueryType.JOIN: lambda sample: self._specifications_join(sample),
            QueryType.SELECT: lambda sample: self._specifications_select(sample),
            QueryType.LOGIC: lambda sample: self._specifications_logic(sample)
        }


    def load_column_types(self):
        for _column_type in QueryType:
            path = os.path.join(QUERY_TYPES_PATH, f"{_column_type.value}.json")
            if not os.path.exists(path):
                continue
            self.column_types[_column_type] = {}
            with open(path) as column_file:
                self.column_types[_column_type] = json.load(column_file)

    def load_from_json(self, filepath: str, source: Source) -> int:
        with open(filepath) as json_file:
            json_samples = json.load(json_file)
        for _json_sample in json_samples:
            sample = self.create_sample_from_json(_json_sample, source)
            self.samples.content.append(sample)
        return len(json_samples)

    def load_russian_from_json(self, filepath: str, id_start: int) -> int:
        with open(filepath) as json_file:
            json_samples = json.load(json_file)
        current_ind = id_start
        for _json_sample in json_samples:
            cusrrent_sample = self.samples.content[current_ind]
            self._verify_translation(cusrrent_sample, _json_sample)
            cusrrent_sample.russian_query = _json_sample['query']
            cusrrent_sample.russian_question = _json_sample['question']
            cusrrent_sample.russian_query_toks = _json_sample['query_toks']
            cusrrent_sample.russian_question_toks = _json_sample['question_toks']
            cusrrent_sample.russian_query_toks_no_values = _json_sample['query_toks_no_value']
            current_ind += 1
        return len(json_samples)

    def load_from_csv(self, filepath: str, source: Source):
        pass

    def import_spider(self):
        dev_path = os.path.join(SPIDER_PATH, 'dev.json')
        train_spider_path = os.path.join(SPIDER_PATH, 'train_spider.json')
        train_others_path = os.path.join(SPIDER_PATH, 'train_others.json')
        dev_size = self.load_from_json(dev_path, Source.SPIDER_DEV),
        train_size = self.load_from_json(train_spider_path, Source.SPIDER_TRAIN),
        other_size = self.load_from_json(train_others_path, Source.SPIDER_TRAIN_OTHERS)
        self.start_indices = {
            Source.SPIDER_DEV: 0,
            Source.SPIDER_TRAIN: dev_size,
            Source.SPIDER_TRAIN_OTHERS: dev_size + train_size
        }

    def import_russocampus(self):
        ru_dev_path = os.path.join(RUSSOCAMPUS_PATH, 'rusp_dev.json')
        ru_train_path = os.path.join(RUSSOCAMPUS_PATH, 'rusp_train.json')
        ru_train_others_path = os.path.join(RUSSOCAMPUS_PATH, 'rusp_train_others.json')
        dev_size = self.load_russian_from_json(ru_dev_path, 0)
        train_size = self.load_russian_from_json(ru_train_path, dev_size)
        _ = self.load_russian_from_json(ru_train_others_path, dev_size + train_size)


    def load(self):
        with open(SAMPLES_PATH, 'rb') as sample_file:
            self.samples.content = pickle.load(sample_file)
        with open(COLUMN_TYPES_PATH, 'rb') as column_type_file:
            self.column_types = pickle.load(column_type_file)
        with open(INDICES_PATH, 'rb') as indices_file:
            self.start_indices = pickle.load(indices_file)

    def save(self):
        with open(SAMPLES_PATH, 'wb') as sample_file:
            pickle.dump(self.samples.content, sample_file)
        with open(COLUMN_TYPES_PATH, 'wb') as column_type_file:
            pickle.dump(self.column_types, column_type_file)
        with open(INDICES_PATH, 'wb') as indices_file:
            pickle.dump(self.start_indices, indices_file)

    def create_sample_from_json(self, sample_json: Dict, source: Source) -> Sample:
        generated_sample = Sample()
        generated_sample.id = len(self.samples.content)
        generated_sample.db_id = sample_json.get('db_id', None)
        generated_sample.source = source
        generated_sample.question = sample_json.get('question', None)
        generated_sample.query = sample_json.get('query', None)
        generated_sample.sql = sample_json.get('question', None)
        generated_sample.query_toks = sample_json.get('query_toks', None)
        generated_sample.query_toks_no_values = sample_json.get('query_toks_no_value', None)
        generated_sample.question_toks = sample_json.get('question_toks', None)
        generated_sample.mentions = self.mention_extractor.get_mentions_from_sample(sample_json)
        generated_sample.specifications = self.extract_specifications(generated_sample)
        return generated_sample

    def extract_specifications(self, sample: Sample) -> Dict:
        specifications = {}
        for _query_type in QueryType:
            specifications[_query_type] = self.EXTRACTION_FUNCTIONS[_query_type](sample)
        return specifications

    def find_all_with_type(self, type: QueryType, subtypes: Optional[List[QuerySubtype]] = None) -> SamplesCollection:
        search_result = SamplesCollection()
        for _sample in self.samples.content:
            sample_subtypes = _sample.specifications[type]
            condition_1 = not subtypes and sample_subtypes
            condition_2 = subtypes and sample_subtypes and all([_s in sample_subtypes for _s in subtypes])
            if condition_1 or condition_2:
                search_result.add(_sample)
        return search_result

    def _verify_translation(self, sample: Sample, translation_json: Dict):
        if sample.db_id != translation_json['db_id']:
            raise ValueError(f"Translation problem: {sample.id} = {sample.question} ({translation_json['question']})")

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
            else:
                specifications += [QuerySubtype.WITHOUT_VALUES]
        if specifications:
            specifications = list(set(specifications))
        return specifications

    def _specifications_simplicity(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        if if_extra_simple(sample):
            return [QuerySubtype.EXTRA_SIMPLE]
        if if_simple(sample):
            return [QuerySubtype.SIMPLE]
        return None

    def _specifications_join(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        if if_single_join(sample):
            return [QuerySubtype.SINGLE_JOIN]
        if if_multi_join(sample):
            return [QuerySubtype.MULTI_JOIN]
        return None

    def _specifications_select(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        if if_multi_select(sample):
            subtypes.append(QuerySubtype.MULTI_SELECT)
        if if_hetero_agg(sample):
            subtypes.append(QuerySubtype.HETERO_AGG)
        if if_mono_agg(sample):
            subtypes.append(QuerySubtype.MONO_AGG)
        if len(subtypes) == 0:
            return None
        return subtypes

    def _specifications_logic(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        and_or = {"and", "or", "или", "и"}
        subtypes = []
        sql_logic_keys = get_logic_keys_from_sql(sample.query_toks_no_values)
        nl_logic_keys = get_logic_keys_from_nl(sample.question_toks) + get_logic_keys_from_nl(sample.russian_question_toks)
        if len(sql_logic_keys) > 0:
            subtypes.append(QuerySubtype.LOGIC_SQL_ALL)
        if len(nl_logic_keys) > 0:
            subtypes.append(QuerySubtype.LOGIC_NL_ALL)
        sql_and_or = and_or.intersection(set(sql_logic_keys))
        nl_and_or = and_or.intersection(set(nl_logic_keys))
        if len(sql_and_or) > 0:
            subtypes.append(QuerySubtype.LOGIC_SQL_AND_OR)
        if len(nl_and_or) > 0:
            subtypes.append(QuerySubtype.LOGIC_NL_AND_OR)
        if ('and' in sql_and_or and 'or' in nl_and_or) or ('or' in sql_and_or and 'and' in nl_and_or):
            subtypes.append(QuerySubtype.LOGIC_VS)
        return subtypes


if __name__ == "__main__":
    araneae = Araneae()
    araneae.import_spider()
    araneae.import_russocampus()

    binary_with_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITH_VALUES])
    binary_without_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITHOUT_VALUES])
    datetimes_with_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITH_VALUES])
    datetimes_without_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITHOUT_VALUES])
    extra_simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.EXTRA_SIMPLE])
    simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.SIMPLE])
    single_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.SINGLE_JOIN])
    multi_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.MULTI_JOIN])
    multi_select = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MULTI_SELECT])
    mono_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MONO_AGG])
    hetero_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.HETERO_AGG])

    test_set_path = '../resources/results/test_sets'
    binary_with_values.save_in_csv(f'{test_set_path}/binary_with_values.csv')
    datetimes_with_values.save_in_csv(f'{test_set_path}/datetimes_with_values.csv')
    binary_without_values.save_in_csv(f'{test_set_path}/binary_without_values.csv')
    datetimes_without_values.save_in_csv(f'{test_set_path}/datetimes_without_values.csv')
    extra_simple.save_in_csv(f'{test_set_path}/extra_simple.csv')
    simple.save_in_csv(f'{test_set_path}/simple.csv')
    single_join.save_in_csv(f'{test_set_path}/single_join.csv')
    multi_join.save_in_csv(f'{test_set_path}/multi_join.csv')
    multi_select.save_in_csv(f'{test_set_path}/multi_select.csv')
    mono_agg.save_in_csv(f'{test_set_path}/mono_agg.csv')
    hetero_agg.save_in_csv(f'{test_set_path}/hetero_agg.csv')

    binary_with_values.save_in_json(f'{test_set_path}/binary_with_values.json')
    datetimes_with_values.save_in_json(f'{test_set_path}/datetimes_with_values.json')
    binary_without_values.save_in_json(f'{test_set_path}/binary_without_values.json')
    datetimes_without_values.save_in_json(f'{test_set_path}/datetimes_without_values.json')
    extra_simple.save_in_json(f'{test_set_path}/extra_simple.json')
    simple.save_in_json(f'{test_set_path}/simple.json')
    single_join.save_in_json(f'{test_set_path}/single_join.json')
    multi_join.save_in_json(f'{test_set_path}/multi_join.json')
    multi_select.save_in_json(f'{test_set_path}/multi_select.json')
    mono_agg.save_in_json(f'{test_set_path}/mono_agg.json')
    hetero_agg.save_in_json(f'{test_set_path}/hetero_agg.json')

    araneae.save()

    a = 7

