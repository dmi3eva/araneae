import os
import pandas as pd
from verification.settings.config import *
from typing import *
import dataframe_image as dfi


def render_table(db: str, table: str, table_content: Tuple):
    # Генерируем DataFrame
    if len(table_content) != 2:
        rows = []
    else:
        rows = table_content[1]
    df = pd.DataFrame(rows, columns=table_content[0])

    # Сохраняем изображения
    db_dir = os.path.join(TABLES_PATH, db)
    table_path = os.path.join(TABLES_PATH, db, f"{table}.png")
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    if not os.path.exists(table_path):
        dfi.export(df, table_path)

    return open(table_path, 'rb')
