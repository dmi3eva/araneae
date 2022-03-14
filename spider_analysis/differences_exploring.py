import json
from typing import *
import pandas as pd

from configure import *
from dto.sample import *
from araneae.wrapper import Araneae


def extract_ids(first_path: str, second_path: str) -> Dict:
    first_df = pd.read_csv(first_path)
    second_df = pd.read_csv(second_path)
    mapping = {_r["id"]: [_r["id"], _r["question"], _r["query"]] for _i, _r in first_df.iterrows()}
    for _i, _row in second_df.iterrows():
        id = _row["id"]
        mapping[id] = [id, _row["question"], _row["query"]]
    first_ids = set(first_df['id'])
    second_ids = set(second_df['id'])
    ids_exists_in_first = first_ids.difference(second_ids)
    ids_exists_in_second = second_ids.difference(first_ids)
    difference = {
        'exists_in_first': [mapping[_id] for _id in ids_exists_in_first],  # TO-DO: to class
        'exists_in_second': [mapping[_id] for _id in ids_exists_in_second]
    }
    return difference


def save_differences(differences, filename, in_first, in_second):
    with open(f"../resources/results/statistics/{filename}.json", 'w') as f:
        json.dump(differences, f)

    rows = []
    for _d in differences['exists_in_first']:
        rows.append({
            'id': _d[0],
            'question': _d[1],
            'query': _d[2],
            'status': in_first
        })
    for _d in differences['exists_in_second']:
        rows.append({
            'id': _d[0],
            'question': _d[1],
            'query': _d[2],
            'status': in_second
        })
    df = pd.DataFrame(data=rows)
    df.to_csv(f"../resources/results/statistics/{filename}.csv")


if __name__ == "__main__":
    # FIRST_FILE_PATH = 'C:\\Users\\forka\PycharmProjects\\araneae\\resources\\results\\test_sets\\csv\\logic_nl_not.csv'
    # SECOND_FILE_PATH = 'C:\\Users\\forka\PycharmProjects\\araneae\\resources\\results\\test_sets\\csv\\logic_sql_not.csv'
    FIRST_FILE_PATH = 'C:\\Users\\forka\PycharmProjects\\araneae\\resources\\results\\test_sets\\csv\\negation.csv'
    SECOND_FILE_PATH = 'C:\\Users\\forka\PycharmProjects\\araneae\\resources\\results\\test_sets\\csv\\negation_old.csv'
    difference_analysis = extract_ids(FIRST_FILE_PATH, SECOND_FILE_PATH)
    # save_differences(difference_analysis, "22_03_10_negation_difference", "Only in NL", "Only in SQL")
    save_differences(difference_analysis, "22_03_14_negation_difference", "Only in NEW", "Only in OLD")

