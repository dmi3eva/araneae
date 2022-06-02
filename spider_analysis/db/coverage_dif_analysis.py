import os
import json
from copy import deepcopy
from configure import *
from typing import *
from utils.spider_connectors import *
from dto.sample import *
from araneae.wrapper import *

EN_FILE = os.path.join(INFO_DIR, 'en_coverage_values.json')
RU_FILE = os.path.join(INFO_DIR, 'ru_coverage_values.json')

with open(EN_FILE, "r") as db_file:
    en = json.load(db_file)

with open(RU_FILE, "r") as db_file:
    ru = json.load(db_file)

content = {
    "dbs": {},
    "tables": {},
    "columns": {},
    "values": {}
}

dif = {
    "train-spider": deepcopy(content),
    "train-others": deepcopy(content),
    "dev": deepcopy(content),
}

for source, content in en.items():
    for entity, values_set in content.items():
        en_set = values_set
        ru_set = ru[source][entity]
        dif[source][entity]["en"] = list(set(en_set) - set(ru_set))
        dif[source][entity]["ru"] = list(set(ru_set) - set(en_set))

result_file = os.path.join(INFO_DIR, 'difference.json')
with open(result_file, "w", encoding='utf-8') as info_file:
    json.dump(dif, info_file, indent=4, ensure_ascii=False)