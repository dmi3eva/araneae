from araneae.wrapper import *


DB_FILE = os.path.join(INFO_DIR, 'db_by_sources.json')
with open(DB_FILE, "r") as db_file:
    db_by_sources = json.load(db_file)

DB_MAPPING = {}
for source, dbs in db_by_sources.items():
    for db in dbs:
        DB_MAPPING[db] = source

def calculate_coverage(araneae: Araneae, language: Language, info_file:str, db_info: dict) -> NoReturn:
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

    for sample in araneae.samples.content:
        if language is Language.RU:
            mentions = sample.russian_mentions
        else:
            mentions = sample.mentions
        source = db_info[sample.db_id]
        info[source]['dbs'].add(sample.db_id)
        for mention in mentions:
            if mention.type is Subquery.FROM:
                info[source]['tables'].add(f"{mention.db}_{mention.table}")
            if mention.type is Subquery.SELECT and mention.column != '*':
                info[source]['columns'].add(f"{mention.db}_{mention.table}_{mention.column}")
            if mention.type is Subquery.WHERE and mention.values is not None:
                for value in mention.values:
                    processed = str(value).replace("'", "").replace('"', "")
                    info[source]['values'].add(f"{mention.db}_{mention.table}_{mention.column}_{processed}")
    for source, content in info.items():
        for entity, values_set in content.items():
            content[entity] = list(values_set)
    with open(info_file, "w") as info_file:
        json.dump(info, info_file, indent=4)


EN_FILE = os.path.join(INFO_DIR, 'en_coverage_values.json')
RU_FILE = os.path.join(INFO_DIR, 'ru_coverage_values.json')

araneae = Araneae()
araneae.load()
calculate_coverage(araneae, Language.EN, EN_FILE, DB_MAPPING)
calculate_coverage(araneae, Language.RU, RU_FILE, DB_MAPPING)