import json
import collections
import sqlite3
import os
from typing import *
from configure import *

REQUEST_MASK = "SELECT \"{column}\" FROM \"{table}\""
TABLES_REQUEST = f"SELECT name FROM sqlite_master WHERE type='table'"

# from IPython.display import HTML, display

# def progress(value, max=100):
#     return HTML("""
#         <progress
#             value='{value}'
#             max='{max}',
#             style='width: 100%'
#         >
#             {value}
#         </progress>
#     """.format(value=value, max=max))

class SpiderDB:
    def __init__(self):
        self.db_path = None
        self.__dbs: Union[List[str], None] = None
        self.__tables: Union[Dict, None] = None
        self.__columns: Union[Dict, None] = None

    def extract_dbs(self) -> List[str]:
        pass

    def extract_tables(self) -> Dict:
        pass

    def extract_columns(self) -> Dict:
        pass

    @property
    def dbs(self) -> List[str]:
        if not self.__dbs:
            self.__dbs = self.extract_dbs()
        return self.__dbs

    @property
    def tables(self) -> Dict:
        if not self.__tables:
            self.__tables = self.extract_tables()
        return self.__tables

    @property
    def columns(self) -> Dict:
        if not self.__columns:
            self.__columns = self.extract_columns()
        return self.__columns

    def execute_request(self, db_id: str, sql: str):
        db = os.path.join(self.db_path, db_id, db_id + ".sqlite")
        conn = sqlite3.connect(db)
        conn.text_factory = lambda b: b.decode(errors='ignore')
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except:
            raise ValueError

    def get_values(self, db: str, table: str, column: str) -> List[str]:
        # Возвращает значения из столбца данной таблицы
        aim_request = REQUEST_MASK.format(table=table, column=column)
        try:
            response = self.execute_request(db, aim_request)
            values = [str(_v[0]) for _v in list(response)]
            return values
        except ValueError:
            print()
            print(f"Problem with {column} in {table} (db = {db}). Request: {aim_request}")
            return []

    def get_db_tables(self, db: str) -> List[str]:
        return self.tables[db]

    def get_db_columns(self, db: str, table: str) -> List[str]:
        return self.columns[db][table]

    def show_table(self, db: str, table: str):
        values_request = f"SELECT * FROM {table}"
        values = self.execute_request(db, values_request)
        column_names = tuple(self.get_db_columns(db, table))
        return column_names, values


class EnSpiderDB(SpiderDB):
    def __init__(self):
        super().__init__()
        self.db_path = SPIDER_DB_PATH
        self.schemes_path = SPIDER_SCHEMES_PATH

    def extract_dbs(self):
        return os.listdir(self.db_path)

    def extract_tables(self) -> Dict:
        with open(self.schemes_path) as table_file:
            schemes = json.load(table_file)
        extracted_tables = {_s['db_id']: _s['table_names_original'] for _s in schemes}
        return extracted_tables

    def extract_columns(self) -> Dict:
        with open(self.schemes_path) as table_file:
            schemes = json.load(table_file)
        columns = {
            _s['db_id']: {
                _table: [] for _table in _s['table_names_original']
            } for _s in schemes
        }
        for _scheme in schemes:
            db_id = _scheme['db_id']
            table_names = _scheme['table_names_original']
            for _column in _scheme["column_names_original"]:
                column_name = _column[1]
                table_name = table_names[_column[0]]
                if column_name == '*':
                    continue
                columns[db_id][table_name].append(column_name)
        return columns


class RuSpiderDBOld(SpiderDB):
    def __init__(self):
        super().__init__()
        self.db_path =RUSSOCAMPUS_DB_PATH_OLD

    def extract_dbs(self):
        return os.listdir(self.db_path)

    def extract_tables(self) -> Dict:
        tables = {}
        for _db in self.dbs:
            extracted_tables = self.execute_request(_db, TABLES_REQUEST)
            tables[_db] = [_t[0] for _t in extracted_tables]
        return tables

    def extract_columns(self) -> Dict:
        columns = {}
        COLUMNS_REQUEST = "PRAGMA table_info({:s});"
        for _db in self.dbs:
            columns[_db] = {}
            for _table in self.tables[_db]:
                extracted_columns = self.execute_request(_db, COLUMNS_REQUEST.format(_table))
                columns[_db][_table] = [_c[1] for _c in extracted_columns]
        return columns


class RuSpiderDB(RuSpiderDBOld):
    def __init__(self):
        super().__init__()
        self.db_path =RUSSOCAMPUS_DB_PATH_NEW
