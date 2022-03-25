import os
import re
import json
import dill as pickle
import pandas as pd
from configure import *
from copy import deepcopy
from typing import *

from utils.common import *
from utils.preprocessing.text import *
from utils.mention_extractor import MentionExtractor
from araneae.settings import *
# from utils.preprocessing.custom_sql import *
# from utils.preprocessing.spider.process_sql import *
from dto.sample import *


class Araneae:
    def __init__(self):
        self.samples: SamplesCollection = SamplesCollection()
        self.column_types = {}
        self.load_column_types()
        self.db_tokens = {
            "all": {"ru": None, "en": None}
        }
        self.db_tokens_multiusing = {
            "all": {"ru": None, "en": None},
            "tables": {"ru": None, "en": None},
            "columns": {"ru": None, "en": None},
            "values": {"ru": None, "en": None}
        }
        self.load_db_tokens()
        self.mention_extractor = MentionExtractor()
        self.start_indices = None
        self.EXTRACTION_FUNCTIONS = {
            QueryType.BINARY: lambda sample: self._specifications_from_mentions(QueryType.BINARY, sample),
            QueryType.DATETIME: lambda sample: self._specifications_from_mentions(QueryType.DATETIME, sample),
            QueryType.SIMPLICITY: lambda sample: self._specifications_simplicity(sample),
            QueryType.JOIN: lambda sample: self._specifications_join(sample),
            QueryType.SELECT: lambda sample: self._specifications_select(sample),
            QueryType.LOGIC: lambda sample: self._specifications_logic(sample),
            QueryType.NL: lambda sample: self._specifications_nl(sample),
            QueryType.NEGATION: lambda sample: self._specifications_negation(sample),
            QueryType.DB: lambda sample: self._specifications_db(sample),
            QueryType.SQL: lambda sample: self._specifications_sql(sample),
            QueryType.WHERE: lambda sample: self._specifications_where(sample),
            QueryType.GROUP_BY: lambda sample: self._specifications_group_by(sample),
            QueryType.ORDER_BY: lambda sample: self._specifications_order_by(sample),
        }

    def load_column_types(self):
        for _column_type in QueryType:
            path = os.path.join(QUERY_TYPES_PATH, f"{_column_type.value}.json")
            if not os.path.exists(path):
                continue
            self.column_types[_column_type] = {}
            with open(path) as column_file:
                self.column_types[_column_type] = json.load(column_file)

    def load_db_tokens(self):
        with open(EN_ENTITIES, "r", encoding='utf-8') as in_file:
            self.db_tokens["all"]["en"] = json.load(in_file)
        with open(EN_MULTIUSING_ENTITIES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["all"]["en"] = json.load(in_file)
        with open(EN_MULTIUSING_TABLES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["tables"]["en"] = json.load(in_file)
        with open(EN_MULTIUSING_COLUMNS, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["columns"]["en"] = json.load(in_file)
        with open(EN_MULTIUSING_VALUES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["values"]["en"] = json.load(in_file)
        with open(RU_ENTITIES, "r", encoding='utf-8') as in_file:
            self.db_tokens["all"]["ru"] = json.load(in_file)
        with open(RU_MULTIUSING_ENTITIES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["all"]["ru"] = json.load(in_file)
        with open(RU_MULTIUSING_TABLES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["tables"]["ru"] = json.load(in_file)
        with open(RU_MULTIUSING_COLUMNS, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["columns"]["ru"] = json.load(in_file)
        with open(RU_MULTIUSING_VALUES, "r", encoding='utf-8') as in_file:
            self.db_tokens_multiusing["values"]["ru"] = json.load(in_file)

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

    def add_specifications(self, extraction_functions: List[QueryType]) -> NoReturn:
        samples_amount = len(self.samples.content)
        for ind, _sample in enumerate(self.samples.content):
            if ind % 10 == 0:
                print(f"{ind} / {samples_amount}")
            _sample.specifications = self.extract_specifications(extraction_functions, _sample)

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
    def extract_specifications(self, query_types: List[QueryType], sample: Sample) -> Dict:
        specifications = {}
        for _query_type in query_types:
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
        selects = re.findall("select", sample.query)
        if len(selects) > 1:
            subtypes.append(QuerySubtype.NESTED)
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
        if contains_logic_set_phrase(sample):
            subtypes.append(QuerySubtype.LOGIC_SET_PHRASE)
        if len(subtypes) == 0:
            return None
        return subtypes

    def _specifications_negation(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        if sample.id == 4467:
            a = 7
        nl = sample_token_processing(sample.question)
        sql = sample_token_processing(sample.query)
        sql_tokens = set([sample_token_processing(_t) for _t in sample.query_toks])
        nl_tokens = set([sample_token_processing(_t) for _t in sample.question_toks])
        negation_nl_keywords = {"no", "not", "dont", "doesnt", "isnt", "arent", "didnt", "except", "never",
                                "without", "non", "nt", "nor", "ignore", "ignoring", "exclude", "excluding"}
        negation_sql_keywords = {"except", "!", "!=", "null"}
        not_equal_keywords = {"no", "not", "dont", "doesnt", "isnt", "arent", "didnt", "!", "!=", "null", "nor", "not"}
        except_keywords = {"except", "without", "exclude", "excluding", "ignore", "ignoring", "exclude", "excluding"}
        negations_in_nl = nl_tokens.intersection(negation_nl_keywords)
        negations_in_sql = sql_tokens.intersection(negation_sql_keywords)
        VALUES_IDS = {1993, 5660, 5664}  # ID of samples in which "No" is part of value
        if len(negations_in_nl) > 0 and sample.id not in VALUES_IDS:
            subtypes.append(QuerySubtype.NEGATION_NL)
        STRUCTURE_IDS = {5516, 5517, 9081, 9082, 9083, 9084, 9085, 9148,
                         1230, 1558, 3520, 3521, 3522, 3523, 4027, 8830}  # Samples with complex structure, not negations
        NULL_IDS = {4460, 4467, 4468, 4480, 4487, 3494, 3526}
        TOKENIZATION_IDS = {609, 610}
        sql_condition_1 = len(negations_in_sql) > 0 or "!=" in sql
        sql_condition_2 = "not in" not in sql or len(negations_in_sql) > 1
        sql_condition_3 = sample.id not in STRUCTURE_IDS
        sql_condition_4 = sample.id not in NULL_IDS and sample.id not in TOKENIZATION_IDS
        if sql_condition_1 and sql_condition_2 and sql_condition_3 and sql_condition_4:
            subtypes.append(QuerySubtype.NEGATION_SQL)
        if len(subtypes) == 0:
            return None
        negations_in_sample = negations_in_nl.union(negations_in_sql)
        if "no more" in nl:
            subtypes.append(QuerySubtype.NEGATION_SET_PHRASE)
        if "never" in nl_tokens:
            subtypes.append(QuerySubtype.NEGATION_NEVER)
        if "not only" in nl_tokens:
            subtypes.append(QuerySubtype.NEGATION_NOT_ONLY)
        if sample.id in [984, 985]:
            subtypes.append(QuerySubtype.NEGATION_COMMON_KNOWLEDGE)
        if len(negations_in_sample.intersection(not_equal_keywords)) > 0:
            subtypes.append(QuerySubtype.NEGATION_NOT_EQUAL)
        if len(negations_in_sample.intersection(except_keywords)) > 0:
            subtypes.append(QuerySubtype.NEGATION_EXCEPT)
        if "neither" in nl_tokens:
            subtypes.append(QuerySubtype.NEGATION_NEITHER_NOR)
        if "ignore" in nl:
            subtypes.append(QuerySubtype.NEGATION_IGNORING)
        if "other than" in nl:
            subtypes.append(QuerySubtype.NEGATION_OTHER_THAN)
        if "outside" in nl:
            subtypes.append(QuerySubtype.NEGATION_OUTSIDE)
        if "any" in nl_tokens or "all" in nl_tokens or "each" in nl_tokens:
            subtypes.append(QuerySubtype.NEGATION_ANY_ALL)
        if "null" in nl_tokens or "null" in sql_tokens:
            subtypes.append(QuerySubtype.NEGATION_NULL)
        if len(subtypes) == 0:
            return None
        return subtypes

    def _specifications_nl(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        if sample.id == "4467":
            a = 7
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

    def _specifications_db(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []

        if contains_db_mentioned(sample, self.db_tokens, Language.EN):
            subtypes.append(QuerySubtype.DB_EN_MENTIONED_BUT_NOT_USED)
        if contains_db_mentioned(sample, self.db_tokens, Language.RU):
            subtypes.append(QuerySubtype.DB_RU_MENTIONED_BUT_NOT_USED)

        if contains_db_hetero(sample, self.db_tokens_multiusing, Language.EN):
            subtypes.append(QuerySubtype.DB_EN_HETERO_AMBIGUITY)
        if contains_db_hetero(sample, self.db_tokens_multiusing, Language.RU):
            subtypes.append(QuerySubtype.DB_RU_HETERO_AMBIGUITY)

        if contains_db_homo_tables(sample, self.db_tokens_multiusing, Language.EN):
            subtypes.append(QuerySubtype.DB_EN_TABLES_AMBIGUITY)
        if contains_db_homo_columns(sample, self.db_tokens_multiusing, Language.EN):
            subtypes.append(QuerySubtype.DB_EN_COLUMNS_AMBIGUITY)
        if contains_db_homo_values(sample, self.db_tokens_multiusing, Language.EN):
            subtypes.append(QuerySubtype.DB_EN_VALUES_AMBIGUITY)

        if contains_db_homo_tables(sample, self.db_tokens_multiusing, Language.RU):
            subtypes.append(QuerySubtype.DB_RU_TABLES_AMBIGUITY)
        if contains_db_homo_columns(sample, self.db_tokens_multiusing, Language.RU):
            subtypes.append(QuerySubtype.DB_RU_COLUMNS_AMBIGUITY)
        if contains_db_homo_values(sample, self.db_tokens_multiusing, Language.RU):
            subtypes.append(QuerySubtype.DB_RU_VALUES_AMBIGUITY)

        return subtypes

    def _specifications_sql(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        sql = sample_token_processing(sample.query)
        if "like" in sql:
            subtypes.append(QuerySubtype.SQL_LIKE)
        if "limit" in sql:
            subtypes.append(QuerySubtype.SQL_LIMIT)
        if "cast" in sql:
            subtypes.append(QuerySubtype.SQL_CAST)
        if "exist" in sql:
            subtypes.append(QuerySubtype.SQL_EXISTS)
        if "null" in sql:
            subtypes.append(QuerySubtype.SQL_NULL)
        if "between" in sql:
            subtypes.append(QuerySubtype.SQL_BETWEEN)
        if "except" in sql:
            subtypes.append(QuerySubtype.SQL_EXCEPT)
        if "having" in sql:
            subtypes.append(QuerySubtype.SQL_HAVING)
        if "distinct" in sql:
            subtypes.append(QuerySubtype.SQL_DISCTINCT)
        if "<" in sql or ">" in sql or "=" in sql or "between" in sql:
            subtypes.append(QuerySubtype.SQL_COMPARE)
        return subtypes

    def _specifications_where(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        where_mentions = [_m for _m in sample.mentions if _m.type is Subquery.WHERE]
        if len(where_mentions) == 1:
            subtypes.append(QuerySubtype.WHERE_MONO)
        if len(where_mentions) == 2:
            subtypes.append(QuerySubtype.WHERE_MULTI)
        return subtypes

    def _specifications_group_by(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        return subtypes

    def _specifications_order_by(self, sample: Sample) -> Optional[List[QuerySubtype]]:
        subtypes = []
        return subtypes

