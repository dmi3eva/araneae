import os
import json
from copy import deepcopy
from configure import *
from utils.spider_connectors import *

DB_FILE = os.path.join(INFO_DIR, 'db_by_sources.json')
INFO_FILE = os.path.join(INFO_DIR, 'sources_stats.json')

content = {
    "dbs": 0,
    "tables": 0,
    "columns": 0,
    "values": 0
}

info = {
    "train-spider": deepcopy(content),
    "train-others": deepcopy(content),
    "dev": deepcopy(content),
}

with open(DB_FILE, "r") as db_file:
    db_by_sources = json.load(db_file)

en_spider = EnSpiderDB()
for source, dbs in db_by_sources.items():
    for db in dbs:
        info[source]['dbs'] += 1
        tables = en_spider.get_db_tables(db)
        info[source]['tables'] += len(tables)

with open(INFO_FILE, "w") as info_file:
    json.dump(info, info_file, indent=4)


