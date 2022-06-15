import os
import json
from configure import *
from typing import *
from utils.nlp import is_russian


def calculate_statistics(filepath: str) -> Dict:
    all_amounts = []
    ru_amounts = []
    en_amounts = []
    with open(filepath, "r", encoding="utf-8") as tokens_file:
        tokens = json.load(tokens_file)
    for _db, _tokens_dict in tokens.items():
        all_tokens = list(_tokens_dict.keys())
        ru_tokens = [_t for _t in all_tokens if is_russian(_t)]
        en_tokens = [_t for _t in all_tokens if not is_russian(_t)]
        all_amounts.append(len(all_tokens))
        ru_amounts.append(len(ru_tokens))
        en_amounts.append(len(en_tokens))
    stat = {
        'all_total': sum(all_amounts),
        'ru_total': sum(ru_amounts),
        'en_total': sum(en_amounts),
        'all_avg': sum(all_amounts) / len(all_amounts),
        'ru_avg': sum(ru_amounts) / len(ru_amounts),
        'en_avg': sum(en_amounts) / len(en_amounts)
    }
    return stat


print('---- ALL ----')
all_en_stat = calculate_statistics(os.path.join(TOKENS_EN_PATH, EN_MULTIUSING_ENTITIES))
all_ru_stat = calculate_statistics(os.path.join(TOKENS_RU_PATH, RU_MULTIUSING_ENTITIES))
print(all_en_stat)
print(all_ru_stat)

print('---- TABLES ----')
all_en_tables = calculate_statistics(os.path.join(TOKENS_EN_PATH, EN_MULTIUSING_TABLES))
all_ru_tables = calculate_statistics(os.path.join(TOKENS_EN_PATH, RU_MULTIUSING_TABLES))
print(all_en_tables)
print(all_ru_tables)

print('---- COLUMNS ----')
all_en_columns = calculate_statistics(os.path.join(TOKENS_EN_PATH, EN_MULTIUSING_COLUMNS))
all_ru_columns = calculate_statistics(os.path.join(TOKENS_EN_PATH, RU_MULTIUSING_COLUMNS))
print(all_en_columns)
print(all_ru_columns)

print('---- VALUES ----')
all_en_values = calculate_statistics(os.path.join(TOKENS_EN_PATH, EN_MULTIUSING_VALUES))
all_ru_values = calculate_statistics(os.path.join(TOKENS_EN_PATH, RU_MULTIUSING_VALUES))
print(all_en_values)
print(all_ru_values)

a = 7