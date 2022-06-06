from araneae.wrapper import *

EN_FILE = os.path.join(INFO_DIR, 'en_coverage_values.json')
RU_FILE = os.path.join(INFO_DIR, 'ru_coverage_values.json')
ALL_EN_FILE = os.path.join(INFO_DIR, 'all_en_entities.json')
ALL_RU_FILE = os.path.join(INFO_DIR, 'all_ru_entities.json')

with open(EN_FILE, "r") as db_file:
    en = json.load(db_file)

with open(RU_FILE, "r") as db_file:
    ru = json.load(db_file)

with open(ALL_EN_FILE, "r") as db_file:
    all_en = json.load(db_file)

with open(ALL_RU_FILE, "r") as db_file:
    all_ru = json.load(db_file)


content = {
    "dbs": [],
    "tables": [],
    "columns": [],
}

dif = {
    "train-spider": deepcopy(content),
    "train-others": deepcopy(content),
    "dev": deepcopy(content),
}

for source, content in en.items():
    for entity, values_set in content.items():
        en_set = values_set
        all_en_set = all_en[source][entity]
        dif[source][entity] = list(set(all_en_set) - set(en_set))

en_result_file = os.path.join(INFO_DIR, 'all_en_difference.json')
with open(en_result_file, "w", encoding='utf-8') as info_file:
    json.dump(dif, info_file, indent=4, ensure_ascii=False)

dif = {
    "train-spider": deepcopy(content),
    "train-others": deepcopy(content),
    "dev": deepcopy(content),
}

for source, content in ru.items():
    for entity, values_set in content.items():
        ru_set = values_set
        all_ru_set = all_ru[source][entity]
        dif[source][entity] = list(set(all_ru_set) - set(ru_set))

ru_result_file = os.path.join(INFO_DIR, 'all_ru_difference.json')
with open(ru_result_file, "w", encoding='utf-8') as info_file:
    json.dump(dif, info_file, indent=4, ensure_ascii=False)
