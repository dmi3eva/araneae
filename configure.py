from os import curdir, path, getcwd

ROOT_PATH = "C:\\Users\\forka\\PycharmProjects\\araneae"

# Results file exploring
MODEL_REPORT_FOLDER = path.join(ROOT_PATH, "resources", "model_eval")
TEST_SET_FOLDER = path.join(ROOT_PATH, "resources", "results", "test_sets", "json")
RESULTS_FOLDER = path.join(ROOT_PATH, "resources", "results", "reports")
ERROR_PATH = path.join(ROOT_PATH, "resources", "results", "reports", "errors.txt")

# Mentions extractor
SCHEMES_PATH = path.join(ROOT_PATH, 'resources', 'datasets', 'spider', 'tables.json')

# Wrapper
SPIDER_PATH = path.join(ROOT_PATH, "resources", "datasets", "spider")
RUSSOCAMPUS_PATH = path.join(ROOT_PATH, "resources", "datasets", "russocampus")
RUSSOCAMPUS_NEW_PATH = path.join(ROOT_PATH, "resources", "datasets", "russocampus_new")

QUERY_TYPES_PATH = path.join(ROOT_PATH, "resources", "query_types")
ARANEAE_PATH = path.join(ROOT_PATH, "resources", "dump", "araneae")

SAMPLES_PATH = path.join(ARANEAE_PATH, 'samples.dat')
COLUMN_TYPES_PATH = path.join(ARANEAE_PATH, 'column_types.dat')
INDICES_PATH = path.join(ARANEAE_PATH, 'indices.dat')

# Profiling
PROF_PATH = path.join(ROOT_PATH, "log", "profiling")

# Verification
SAMPLES_JSON = path.join(ROOT_PATH, "resources", "datasets", "araneae", "araneae.json")
SAMPLES_PARAPHRASED_PATH = path.join(ROOT_PATH, "resources", "datasets", "araneae", "paraphrased.json")
DUMMY_PARAPHRASED_PATH = path.join(ROOT_PATH, "resources", "datasets", "araneae", "paraphrased_dummy.json")

# Tokens exploring
MIN_TOKEN_LENGTH = 3
MAX_VALUES_IN_COLUMNS = 100
TOKENS_RU_PATH = path.join(ROOT_PATH, "resources", "results", "tokens", "tokens_info_ru.json")
TOKENS_EN_PATH = path.join(ROOT_PATH, "resources", "results", "tokens", "tokens_info_en.json")
RU_ENTITIES = path.join(ROOT_PATH, "resources", "results", "tokens", "all_without_db", "ru.json")
EN_ENTITIES = path.join(ROOT_PATH, "resources", "results", "tokens", "all_without_db", "en.json")
RU_MULTIUSING_ENTITIES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "all_without_db", "ru.json")
EN_MULTIUSING_ENTITIES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "all_without_db", "en.json")
RU_MULTIUSING_TABLES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "tables", "ru.json")
EN_MULTIUSING_TABLES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "tables", "en.json")
RU_MULTIUSING_COLUMNS = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "columns", "ru.json")
EN_MULTIUSING_COLUMNS = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "columns", "en.json")
RU_MULTIUSING_VALUES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "values", "ru.json")
EN_MULTIUSING_VALUES = path.join(ROOT_PATH, "resources", "results", "tokens", "multiusing", "values", "en.json")


# Spider connectors
SPIDER_DB_PATH = path.join(ROOT_PATH, "resources", "datasets", "spider", "database")
RUSSOCAMPUS_DB_PATH = path.join(ROOT_PATH, "resources", "datasets", "russocampus", "merged_database")
SPIDER_SCHEMES_PATH = path.join(ROOT_PATH, "resources", "datasets", "spider", "tables.json")


# Similarity tools
RU_EMBEDDING_MODEL = "araneum_none_fasttextcbow_300_5_2018"
#  RU_EMBEDDING_MODEL = "ruwikiruscorpora-nobigrams_upos_skipgram_300_5_2018"
EN_EMBEDDING_MODEL_DIR = path.join(ROOT_PATH, "resources", "models", "embedders", "en")
RU_EMBEDDING_MODEL_DIR = path.join(ROOT_PATH, "resources", "models", "embedders", "ru")
RU_EMBEDDING_MODEL_ARCHIVE = path.join(RU_EMBEDDING_MODEL_DIR, f"{RU_EMBEDDING_MODEL}.tgz")
# RU_EMBEDDING_MODEL_ARCHIVE = path.join(RU_EMBEDDING_MODEL_DIR, f"{RU_EMBEDDING_MODEL}.vec.gz")
RU_EMBEDDING_MODEL_PATH = path.join(RU_EMBEDDING_MODEL_DIR, f"{RU_EMBEDDING_MODEL}.model")
RU_EMBEDDING_MODEL_URL = f"https://rusvectores.org/static/models/rusvectores4/fasttext/{RU_EMBEDDING_MODEL}.tgz"
# RU_EMBEDDING_MODEL_URL = f"https://rusvectores.org/static/models/rusvectores4/unigrams/{RU_EMBEDDING_MODEL}.vec.gz"