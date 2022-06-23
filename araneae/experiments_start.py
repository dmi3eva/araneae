from wrapper import *


TEST_SET_PATH_CSV  = '../resources/results/test_sets/csv'
TEST_SET_PATH_JSON = '../resources/results/test_sets/json'
SUBTYPES_PATH_CSV = '../resources/results/subtypes'


def save(test_sets_collections: Dict[str, SamplesCollection]):
    for name, _test_set in test_sets_collections.items():
        csv_name = f"{name}.csv"
        json_name = f"{name}.json"
        _test_set.save_in_csv(f'{TEST_SET_PATH_CSV}/{csv_name}')
        _test_set.save_in_json(f'{TEST_SET_PATH_JSON}/{json_name}')

#######################################################
############  Starting   ##############################
#######################################################


araneae = Araneae()
araneae.import_russocampus()
araneae.save_in_json()
araneae.save()

