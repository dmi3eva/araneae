from collections import Counter
from utils.spider_connectors import *
from utils.spider_analysis import *


def get_column_sizes_statistics(connector: SpiderDB, verbose=False) -> Tuple[NumericalStatistics, NumericalStatistics]:
    """
    Returns sizes of tables, amount of unique values in the tables
    """
    all_sizes = []
    unique_sizes = []
    nan_amount = 0
    for _triple in connector.triples:
        db, table, column = _triple
        values = connector.get_values(db, table, column)
        all_sizes.append(len(values))
        if len(values) == 0 and verbose:
            print(f"Zero values: {db} {table} {column}")
        unique_values = set(values)
        if len(unique_values) == 1 and str(values[0]).lower() == 'none':
            if verbose:
                print(f"One unique values: {db} {table} {column} -> {values[0]}")
            nan_amount += 1
        unique_sizes.append(len(unique_values))
    all_counter = Counter(all_sizes)
    unique_counter = Counter(unique_sizes)
    print(f"Only nan: {nan_amount}")
    return NumericalStatistics(all_counter), NumericalStatistics(unique_counter)


def get_tables_sizes_statistics(connector: SpiderDB, verbose=False) -> NumericalStatistics:
    """
    Returns sizes of tables, amount of unique values in the tables
    """
    all_sizes = []
    for db in connector.dbs:
        for table in connector.get_db_tables(db):
            size = 0
            for column in connector.get_db_columns(db):
                values = connector.get_values(db, table, column)
                size = max(size, len(values))
            all_sizes.append(size)
    all_counter = Counter(all_sizes)
    return NumericalStatistics(all_counter)


def get_entities_sizes_statistics(connector: SpiderDB) -> Tuple[NumericalStatistics, NumericalStatistics]:
    """
    Returns sizes of values in symbols and in tokens
    """
    all_sizes = []
    unique_sizes = []
    all_values = set()
    total = len(connector.triples)
    nans_amount = 0
    for ind, _triple in enumerate(connector.triples):
        if ind % 500 == 0:
            print(f"{ind} / {total}")
        db, table, column = _triple
        values = connector.get_values(db, table, column)
        current_nan = len(list(filter(lambda x: len(str(x)) == 0 or str(x).lower() == 'nan', values)))
        nans_amount += current_nan
        unique_values = set(values)
        all_values = all_values.union(unique_values)
    all_values_list = list(all_values)
    print(f"NaN's amount is {nans_amount}")
    print(f"Amount of unique values is {len(all_values_list)}")

    symbol_sizes = [len(entity) for entity in all_values_list]
    print(f"Longest value is \"{all_values_list[symbol_sizes.index(max(symbol_sizes))]}\"")

    token_sizes = [len(entity.split(' ')) for entity in all_values_list]
    print(f"Longest value is \"{all_values_list[token_sizes.index(max(token_sizes))]}\"")

    print(f"Average symbols size if {sum(symbol_sizes) / len(all_values_list)}")
    print(f"Average tokens size if {sum(token_sizes) / len(all_values_list)}")
    symbols_counter = Counter(symbol_sizes)
    tokens_counter = Counter(token_sizes)
    return NumericalStatistics(symbols_counter), NumericalStatistics(tokens_counter)


def get_russian_entities_sizes_statistics(connector: SpiderDB) -> Tuple[NumericalStatistics, NumericalStatistics]:
    """
    Returns sizes of values in symbols and in tokens
    """
    all_sizes = []
    unique_sizes = []
    all_values = set()
    total = len(connector.triples)
    for ind, _triple in enumerate(connector.triples):
        if ind % 500 == 0:
            print(f"{ind} / {total}")
        db, table, column = _triple
        values = connector.get_values(db, table, column)
        unique_values = set(values)
        all_values = all_values.union(unique_values)
    all_values_list = [_v for _v in list(all_values) if is_russian(_v)]
    print(f"Amount of unique values is {len(all_values_list)}")

    symbol_sizes = [len(entity) for entity in all_values_list]
    print(f"Longest value is \"{all_values_list[symbol_sizes.index(max(symbol_sizes))]}\"")

    token_sizes = [len(entity.split(' ')) for entity in all_values_list]
    print(f"Longest value is \"{all_values_list[token_sizes.index(max(token_sizes))]}\"")

    print(f"Average symbols size if {sum(symbol_sizes) / len(all_values_list)}")
    print(f"Average tokens size if {sum(token_sizes) / len(all_values_list)}")
    symbols_counter = Counter(symbol_sizes)
    tokens_counter = Counter(token_sizes)
    return NumericalStatistics(symbols_counter), NumericalStatistics(tokens_counter)


def is_russian(text: str) -> bool:
    ru_alphabet = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
    size = len(text)
    if size == 0:
        return False
    if text[0] in ru_alphabet or text[-1] in ru_alphabet or text[size // 2] in ru_alphabet:
        return True
    return False


def extract_russians(connector: SpiderDB) -> List[Tuple]:
    """
    Returns sizes of values in symbols and in tokens
    """
    russian_fours = []
    total = len(connector.triples)
    for ind, _triple in enumerate(connector.triples):
        if ind % 500 == 0:
            print(f"{ind} / {total}")
        db, table, column = _triple
        values = connector.get_values(db, table, column)
        russian_values = [_v for _v in values if is_russian(_v)]
        if len(russian_values) > 0:
            russian_fours.append((db, table, column, russian_values))
    return russian_fours
