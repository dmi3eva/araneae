from copy import deepcopy
from utils.spider_connectors import *

DB_FILE = os.path.join(INFO_DIR, 'db_by_sources.json')


def calculate_entities_with_values(spider: SpiderDB, info_file) -> NoReturn:
    content = {
        "dbs": set(),
        "tables": set(),
        "columns": set(),
        "values": set()
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
            info[source]['dbs'].add(db)
            tables = spider.get_db_tables(db)
            for table in tables:
                info[source]['tables'].add(f"{db}#{table}")
                columns = spider.get_db_columns(db, table)
                for column in columns:
                    info[source]['columns'].add(f"{db}#{table}#{column}")

    for source, content in info.items():
        for entity, values_set in content.items():
            content[entity] = list(values_set)

    with open(info_file, "w") as info_file:
        json.dump(info, info_file, indent=4)


ALL_EN_FILE = os.path.join(INFO_DIR, 'all_en_entities.json')
ALL_RU_FILE = os.path.join(INFO_DIR, 'all_ru_entities.json')

en_spider = EnSpiderDB()
ru_spider = RuSpiderDB()

calculate_entities_with_values(en_spider, ALL_EN_FILE)
calculate_entities_with_values(ru_spider, ALL_RU_FILE)


