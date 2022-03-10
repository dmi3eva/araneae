import os
import json
import dill as pickle
import pandas as pd
from configure import *
from copy import deepcopy
from typing import *

from utils.common import *
from utils.mention_extractor import MentionExtractor
from araneae.settings import *
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
            QueryType.LOGIC: lambda sample: self._specifications_logic(sample),
            QueryType.NL: lambda sample: self._specifications_nl(sample)
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


    def add_specifications(self):
        for _sample in self.samples.content:
            _sample.specifications = self.extract_specifications(_sample)

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
        return generated_sample

    @profile
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
        and_keys = {"and", "и"}
        or_keys = {"or", "или"}
        and_or = {"and", "or", "или", "и", "intersect", "union"}
        subtypes = []
        sql_logic_keys = get_logic_keys_from_sql(sample.query_toks_no_values)
        nl_logic_keys = get_logic_keys_from_nl(sample.question_toks) + get_logic_keys_from_nl(sample.russian_question_toks)
        if len(sql_logic_keys) > 0:
            subtypes.append(QuerySubtype.LOGIC_SQL_ALL)
        if len(nl_logic_keys) > 0:
            subtypes.append(QuerySubtype.LOGIC_NL_ALL)
        sql_and_or = and_or.intersection(set(sql_logic_keys))
        nl_and_or = and_or.intersection(set(nl_logic_keys))
        nl_and = and_keys.intersection(set(nl_logic_keys))
        nl_or = or_keys.intersection(set(nl_logic_keys))
        if len(sql_and_or) > 0:
            subtypes.append(QuerySubtype.LOGIC_SQL_AND_OR)
        if len(nl_and_or) > 0:
            subtypes.append(QuerySubtype.LOGIC_NL_AND_OR_OR)
        if len(nl_and) > 0 and len(nl_or) > 0:
            subtypes.append(QuerySubtype.LOGIC_NL_AND_AND_OR)
        condition_1 = ('and' in sql_and_or or "intersect" in sql_and_or) and ('or' in nl_and_or)
        condition_2 = ('or' in sql_and_or or "union" in sql_and_or) and ('and' in nl_and_or)
        """
        Don't fit:
            1. Union = SELECT for several columns
            2. AND & OR are both in NL
            3. UNION = WHERE with AND
        """
        if (condition_1 or condition_2) and sample.id in [726, 1902, 2387, 2402]:   # TO-DO
            subtypes.append(QuerySubtype.LOGIC_VS)
        return subtypes

    def _specifications_nl(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        sentences_amount = get_sentences_amount(sample.question)
        sql_tokens = len(sample.query_toks)
        nl_tokens = len(sample.question_toks)
        if sentences_amount > 1:
            subtypes.append(QuerySubtype.NL_SEVERAL_SENTENCES)
        if sql_tokens / nl_tokens >= SQL_NL_THRESHOLD:
            subtypes.append(QuerySubtype.NL_SHORT_SQL_LONG)
        if nl_tokens / sql_tokens >= NL_SQL_THRESHOLD:
            subtypes.append(QuerySubtype.NL_LONG_SQL_SHORT)
        if nl_tokens >= LONG_NL:
            subtypes.append(QuerySubtype.NL_LONG)
        return subtypes


if __name__ == "__main__":
    araneae = Araneae()
    araneae.import_spider()
    araneae.import_russocampus()
    araneae.add_specifications()

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
    logic_vice_versa = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_VS])
    logic_all_nl_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL, QuerySubtype.LOGIC_NL_ALL])
    logic_andor_nl_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_AND_OR, QuerySubtype.LOGIC_NL_AND_OR_OR])
    logic_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL])
    logic_and_with_or_nl = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_NL_AND_AND_OR])
    nl_several_sentences = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SEVERAL_SENTENCES])
    nl_short_sql_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SHORT_SQL_LONG])
    nl_long_sql_short = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG_SQL_SHORT])
    nl_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG])

    test_set_path_csv = '../resources/results/test_sets/csv'
    binary_with_values.save_in_csv(f'{test_set_path_csv}/binary_with_values.csv')
    datetimes_with_values.save_in_csv(f'{test_set_path_csv}/datetimes_with_values.csv')
    binary_without_values.save_in_csv(f'{test_set_path_csv}/binary_without_values.csv')
    datetimes_without_values.save_in_csv(f'{test_set_path_csv}/datetimes_without_values.csv')
    extra_simple.save_in_csv(f'{test_set_path_csv}/extra_simple.csv')
    simple.save_in_csv(f'{test_set_path_csv}/simple.csv')
    single_join.save_in_csv(f'{test_set_path_csv}/single_join.csv')
    multi_join.save_in_csv(f'{test_set_path_csv}/multi_join.csv')
    multi_select.save_in_csv(f'{test_set_path_csv}/multi_select.csv')
    mono_agg.save_in_csv(f'{test_set_path_csv}/mono_agg.csv')
    hetero_agg.save_in_csv(f'{test_set_path_csv}/hetero_agg.csv')
    logic_vice_versa.save_in_csv(f'{test_set_path_csv}/logic_vice_versa.csv')
    logic_all_nl_sql.save_in_csv(f'{test_set_path_csv}/logic_all_nl_sql.csv')
    logic_andor_nl_sql.save_in_csv(f'{test_set_path_csv}/logic_andor_nl_sql.csv')
    logic_sql.save_in_csv(f'{test_set_path_csv}/logic_sql.csv')
    logic_and_with_or_nl.save_in_csv(f'{test_set_path_csv}/logic_and_with_or_nl.csv')
    nl_several_sentences.save_in_csv(f'{test_set_path_csv}/nl_several_sentences.csv')
    nl_short_sql_long.save_in_csv(f'{test_set_path_csv}/nl_short_sql_long.csv')
    nl_long_sql_short.save_in_csv(f'{test_set_path_csv}/nl_long_sql_short.csv')
    nl_long.save_in_csv(f'{test_set_path_csv}/nl_long.csv')

    test_set_path_json = '../resources/results/test_sets/json'
    binary_with_values.save_in_json(f'{test_set_path_json}/binary_with_values.json')
    datetimes_with_values.save_in_json(f'{test_set_path_json}/datetimes_with_values.json')
    binary_without_values.save_in_json(f'{test_set_path_json}/binary_without_values.json')
    datetimes_without_values.save_in_json(f'{test_set_path_json}/datetimes_without_values.json')
    extra_simple.save_in_json(f'{test_set_path_json}/extra_simple.json')
    simple.save_in_json(f'{test_set_path_json}/simple.json')
    single_join.save_in_json(f'{test_set_path_json}/single_join.json')
    multi_join.save_in_json(f'{test_set_path_json}/multi_join.json')
    multi_select.save_in_json(f'{test_set_path_json}/multi_select.json')
    mono_agg.save_in_json(f'{test_set_path_json}/mono_agg.json')
    hetero_agg.save_in_json(f'{test_set_path_json}/hetero_agg.json')
    logic_vice_versa.save_in_json(f'{test_set_path_json}/logic_vice_versa.json')
    logic_all_nl_sql.save_in_json(f'{test_set_path_json}/logic_all_nl_sql.json')
    logic_andor_nl_sql.save_in_json(f'{test_set_path_json}/logic_andor_nl_sql.json')
    logic_sql.save_in_json(f'{test_set_path_json}/logic_sql.json')
    logic_and_with_or_nl.save_in_json(f'{test_set_path_json}/logic_and_with_or_nl.json')
    nl_several_sentences.save_in_json(f'{test_set_path_json}/nl_several_sentences.json')
    nl_short_sql_long.save_in_json(f'{test_set_path_json}/nl_short_sql_long.json')
    nl_long_sql_short.save_in_json(f'{test_set_path_json}/nl_long_sql_short.json')
    nl_long.save_in_json(f'{test_set_path_csv}/nl_long.json')

    araneae.save()
    a = 7
