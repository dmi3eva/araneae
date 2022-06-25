import os
import json
import pandas

from configure import *
from araneae.wrapper import Araneae
from araneae.settings import *
from dto.sample import *


def make_test_set_report(araneae: Araneae, source: Source) -> Dict[str, Dict[str, float]]:
    report = {}
    test_set_names = [_f for _f in os.listdir(TEST_SET_FOLDER) if _f.endswith('.json')]
    model_report_names = [_f for _f in os.listdir(MODEL_REPORT_FOLDER) if _f.endswith('.json')]
    for _model in model_report_names:
        model_path = os.path.join(MODEL_REPORT_FOLDER, _model)
        report[_model] = {}
        for _test_set in test_set_names:
            test_set_path = os.path.join(TEST_SET_FOLDER, _test_set)
            accuracy, test_size, all_size = estimate(araneae, source, test_set_path, model_path)
            report[_model][_test_set] = {
                "accuracy": accuracy,
                "size (DEV)": test_size,
                "size (All)": all_size
            }
    return report


def estimate(araneae: Araneae, source: Source, test_set_path: str, model_path: str) -> (float, int):
    with open(test_set_path, "r", encoding='utf-8') as json_file:
        test_set = json.load(json_file)
    with open(model_path, "r", encoding='utf-8') as json_file:
        model_report = json.load(json_file)
    executed = model_report['per_item']
    template_path = None
    if len(executed) == 9906:
        template_path = JSON_ALL
    if len(executed) == 213:
        template_path = JSON_NEW_ALL
    if len(executed) == 1086:
        template_path = JSON_ALL_DEV
    if len(executed) == 1034:
        template_path = JSON_DEV
    if not template_path:
        mapping = make_mapping(araneae, source, executed)
        print("Look at line 44")
    else:
        mapping = make_mapping_as_in_file(executed, template_path)
    correct = 0
    size = 0
    for _sample in test_set:
        id = _sample['id']
        if id not in mapping.keys():
            continue
        size += 1
        if mapping[id]['exact']:
            correct += 1
    if size > 0:
        return correct / size, size, len(test_set)
    return None, size, len(test_set)


def enumerate_samples(araneae: Araneae, source: Source, samples: List[dict]):
    start_index = araneae.start_indices[source]
    for ind, sample in enumerate(samples):
        sample['id'] = start_index + ind


def make_mapping(araneae: Araneae, source: Source, samples: List[dict]) -> dict:
    """"
    Returns mapping:
        id -> sample from eval
    Example:
        "D_0001" -> {}
    """
    mapping = {}
    PREFIX = {
        Source.SPIDER_DEV: 'D',
        Source.SPIDER_TRAIN: "TS",
        Source.SPIDER_TRAIN_OTHERS: "TO"
    }
    start_index = araneae.start_indices[source]
    for ind, sample in enumerate(samples):
        id = start_index + ind
        mapping[f"{PREFIX[source]}_{str(id).zfill(4)}"] = sample
        # mapping[id] = sample
    return mapping


def make_mapping_as_in_file(eval_samples: List[dict], filepath: str) -> dict:
    """"
    Returns mapping:
        id -> sample from eval
    Example:
        "D_0001" -> {}
    """
    mapping = {}
    with open(filepath, "r", encoding='utf-8') as template_file:
        template_samples = json.load(template_file)
    for ind, json_sample in enumerate(template_samples):
        id = json_sample["id"]
        mapping[id] = eval_samples[ind]
    return mapping


def save_sql_statistics(report, filename):
    with open(f"{RESULTS_FOLDER}/{filename}.json", 'w') as f:
        json.dump(report, f)

    data = []
    for _model, _result in report.items():
        for _test_set, _result in _result.items():
            row = {
                "Model": str(_model),
                "Test-set": str(_test_set),
                "Accuracy": _result["accuracy"],
                "Size (DEV)": _result["size (DEV)"],
                "Size (All)": _result["size (All)"]
            }
            data.append(row)
    df = pandas.DataFrame(data=data)
    df.to_csv(f"{RESULTS_FOLDER}/{filename}.csv")


if __name__ == "__main__":
    araneae = Araneae()
    araneae.load()
    report = make_test_set_report(araneae, Source.SPIDER_DEV)
    save_sql_statistics(report, "2022-06-25")
