import json
from typing import *
from utils.spider_connectors import *

DIF_FILE = "difference.json"


def update_dif(change: Dict, db: str, table: str, column: str, values: List[str]) -> Dict:
    if db not in change.keys():
        change[db] = {}
    if table not in change[db].keys():
        change[db][table] = {}
    change[db][table][column] = values
    return change


ru_spider = RuSpiderDB()
en_spider = EnSpiderDB()

dif_content = {
    "to_remove": {},
    "to_add": {}
}

ru_triples = ru_spider.triples

for _ru_triple in ru_triples:
    ru_values = set(ru_spider.get_values(*_ru_triple))
    en_values = set(en_spider.get_values(*_ru_triple))
    to_add = ru_values.difference(en_values)
    to_remove = en_values.difference(ru_values)
    db, table, column = _ru_triple
    if len(to_add) > 0:
        values = sorted(list(to_add))
        dif_content["to_add"] = update_dif(dif_content["to_add"], db, table, column, values)
    if len(to_remove) > 0:
        values = sorted(list(to_add))
        dif_content["to_remove"] = update_dif(dif_content["to_remove"], db, table, column, values)
    debug = None

with open(DIF_FILE, "w") as dif_file:
    json.dump(dif_content, dif_file)