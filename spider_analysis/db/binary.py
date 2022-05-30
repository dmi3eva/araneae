import os
import json
from araneae.wrapper import Araneae
from utils.spider_connectors import *
from configure import *
from dto.sample import *


CURRENT_TYPE = 'binary-antonyms'
BINARY_PATH = os.path.join(QUERY_TYPES_PATH, 'binary.json')
ANALYSIS_PATH = os.path.join(ROOT_PATH, 'resources', 'results', 'reports', 'binary', f"{CURRENT_TYPE}.txt")


with open(BINARY_PATH, "r", encoding='utf-8') as file_input:
    binary = json.load(file_input)


current_triples = []
ru_spider = RuSpiderDB()
for db, db_content in binary.items():
    for table,table_content in db_content.items():
        for column, column_content in table_content.items():
            if column_content["type"] == 'binary-antonyms':
                current_triples.append(Triple(db, table, column))

with open(ANALYSIS_PATH, 'w', encoding='utf-8') as anf:
    for _triple in current_triples:
        values = ru_spider.get_values(_triple.db, _triple.table, _triple.column)
        values = list(set(values))
        anf.writelines(str(_triple))
        anf.write('\n')
        for _value in values:
            anf.writelines(f"    {_value}\n")

