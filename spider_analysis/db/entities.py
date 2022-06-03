from copy import deepcopy
from utils.spider_connectors import *

DB_FILE = os.path.join(INFO_DIR, 'db_by_sources.json')


def calculate_entites(spider: SpiderDB, info_file) -> NoReturn:
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

    for source, dbs in db_by_sources.items():
        for db in dbs:
            info[source]['dbs'] += 1
            tables = spider.get_db_tables(db)
            info[source]['tables'] += len(tables)
            for table in tables:
                columns = spider.get_db_columns(db, table)
                info[source]['columns'] += len(columns)
                for column in columns:
                    values = spider.get_values(db, table, column)
                    info[source]['values'] += len(values)

    with open(info_file, "w") as info_file:
        json.dump(info, info_file, indent=4)


EN_FILE = os.path.join(INFO_DIR, 'en_entities.json')
RU_FILE = os.path.join(INFO_DIR, 'ru_entities.json')

en_spider = EnSpiderDB()
ru_spider = RuSpiderDB()

calculate_entites(en_spider, EN_FILE)
calculate_entites(ru_spider, RU_FILE)


