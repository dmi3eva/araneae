from araneae.wrapper import Araneae
from utils.spider_connectors import *
from dto.sample import *
from dataclasses import dataclass
from typing import *
from enum import Enum
import json
from configure import *
from spider_analysis.db.tables_sizes import is_russian


def extract_multiusing_entities(path_from: str, path_to: str) -> NoReturn:
    with open(path_from, "r", encoding='utf-8') as file_from:
        tokens = json.load(file_from)

    multiusing = {}
    for token, token_description in tokens.items():
        db_desriptions = token_description['db']
        for db, tokens_usings in db_desriptions.items():
            multiusing[db] = multiusing.get(db, {})
            different_usings = [_u for _u in tokens_usings if _u['type'] != 'DB']  # Excluding DB's
            if len(different_usings) > 1:
                multiusing[db][token] = different_usings

    with open(path_to, "w", encoding='utf-8') as file_from:
        json.dump(multiusing, file_from, ensure_ascii=False)


def extract_entities(path_from: str, path_to: str) -> NoReturn:
    with open(path_from, "r", encoding='utf-8') as file_from:
        tokens = json.load(file_from)

    multiusing = {}
    for token, token_description in tokens.items():
        db_desriptions = token_description['db']
        for db, tokens_usings in db_desriptions.items():
            multiusing[db] = multiusing.get(db, {})
            different_usings = [_u for _u in tokens_usings if _u['type'] != 'DB']  # Excluding DB's
            multiusing[db][token] = different_usings

    with open(path_to, "w", encoding='utf-8') as file_from:
        json.dump(multiusing, file_from, ensure_ascii=False)


def extract_tables_entities(path_from: str, path_to: str) -> NoReturn:
    with open(path_from, "r", encoding='utf-8') as file_from:
        tokens = json.load(file_from)

    multiusing = {}
    for token, token_description in tokens.items():
        db_desriptions = token_description['db']
        for db, tokens_usings in db_desriptions.items():
            different_usings = [_u for _u in tokens_usings if _u['type'] == 'TABLE']  # Excluding DB's
            multiusing[db] = multiusing.get(db, {})  # TODO
            if len(different_usings) > 1:
                multiusing[db][token] = different_usings

    with open(path_to, "w", encoding='utf-8') as file_from:
        json.dump(multiusing, file_from, ensure_ascii=False)


def extract_columns_entities(path_from: str, path_to: str) -> NoReturn:
    with open(path_from, "r", encoding='utf-8') as file_from:
        tokens = json.load(file_from)

    multiusing = {}
    for token, token_description in tokens.items():
        db_desriptions = token_description['db']
        for db, tokens_usings in db_desriptions.items():
            different_usings = [_u for _u in tokens_usings if _u['type'] == 'COLUMN']  # Excluding DB's
            multiusing[db] = multiusing.get(db, {})  # TODO
            if len(different_usings) > 1:
                multiusing[db][token] = different_usings

    with open(path_to, "w", encoding='utf-8') as file_from:
        json.dump(multiusing, file_from, ensure_ascii=False)


def extract_values_entities(path_from: str, path_to: str) -> NoReturn:
    with open(path_from, "r", encoding='utf-8') as file_from:
        tokens = json.load(file_from)

    multiusing = {}
    for token, token_description in tokens.items():
        db_desriptions = token_description['db']
        for db, tokens_usings in db_desriptions.items():
            different_usings = [_u for _u in tokens_usings if _u['type'] == 'VALUE']  # Excluding DB's
            multiusing[db] = multiusing.get(db, {})  # TODO
            if len(different_usings) > 1:
                multiusing[db][token] = different_usings
    make_analysis(multiusing)
    with open(path_to, "w", encoding='utf-8') as file_from:
        json.dump(multiusing, file_from, ensure_ascii=False)


def make_analysis(multiusing):
    amounts_in_db = []
    tokens_amounts = []
    russian_amounts = []
    for db, content in multiusing.items():
        amounts_in_db.append(len(content))
        russian_values = [_v for _v in content if is_russian(_v)]
        russian_amounts.append(len(russian_values))
        tokens_amounts += [len(_v) for _v in content]
    print(f'There are condfused {sum(tokens_amounts)} tokens')
    print(f'... russian tokens: {sum(russian_amounts)} ot them.')
    print(f'Every token is encountering  {sum(tokens_amounts) / len(tokens_amounts)} ones in average.')
    print(f'Every database contains {sum(amounts_in_db) / len(amounts_in_db)} tokens in average.')


if __name__ == "__main__":
    extract_entities(TOKENS_EN_PATH, EN_ENTITIES)
    extract_entities(TOKENS_RU_PATH, RU_ENTITIES)

    extract_multiusing_entities(TOKENS_EN_PATH, EN_MULTIUSING_ENTITIES)
    extract_multiusing_entities(TOKENS_RU_PATH, RU_MULTIUSING_ENTITIES)

    extract_tables_entities(TOKENS_EN_PATH, EN_MULTIUSING_TABLES)
    extract_tables_entities(TOKENS_RU_PATH, RU_MULTIUSING_TABLES)

    extract_columns_entities(TOKENS_EN_PATH, EN_MULTIUSING_COLUMNS)
    extract_columns_entities(TOKENS_RU_PATH, RU_MULTIUSING_COLUMNS)

    extract_values_entities(TOKENS_EN_PATH, EN_MULTIUSING_VALUES)
    extract_values_entities(TOKENS_RU_PATH, RU_MULTIUSING_VALUES)
