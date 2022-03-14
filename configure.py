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