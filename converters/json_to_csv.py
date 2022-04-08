import os
import json
import pandas as pd
from configure import *

json_path = os.path.join(SPIDER_PATH, "dev.json")
with open(json_path, "r", encoding="utf-8") as json_file:
    data_json = json.load(json_file)

data_list = []
for ind, _sample in enumerate(data_json):
    _row = {
        "id": f"D_{str.zfill(str(ind + 1), 4)}",
        "en": _sample["question"],
        "ru": "",
        "sql_en": _sample["query"],
        "sql_ru": "",
        "db_id": _sample["db_id"],
        "ru_corrected": "",
        "sql_ru_corrected": "",
        "source": "dev"
    }
    data_list.append(_row)

data_df = pd.DataFrame(data=data_list)

csv_file = os.path.join(RUSSOCAMPUS_NEW_PATH, "dev_1034.csv")
data_df.to_csv(csv_file, index=False)

xslx_file = os.path.join(RUSSOCAMPUS_NEW_PATH, "dev_1034.xlsx")
data_df.to_excel(xslx_file, index=False)