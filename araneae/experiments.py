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

########################################################
#############  Starting   ##############################
########################################################

# First start
araneae = Araneae()

# araneae.import_spider()
araneae.import_russocampus()

araneae.save_in_json()
araneae.save()

# # Other starts
# araneae = Araneae()
# araneae.load()

########################################################
#############  Experiments   ##############################
########################################################

#########################################################################################
# # DB
# db_pipeline = [QueryType.DB]
# araneae.add_specifications(db_pipeline)
#
# db_en_mentioned = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_EN_MENTIONED_BUT_NOT_USED])
# db_en_hetero = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_EN_HETERO_AMBIGUITY])
# db_en_tables = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_EN_TABLES_AMBIGUITY])
# db_en_columns = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_EN_COLUMNS_AMBIGUITY])
# db_en_values = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_EN_VALUES_AMBIGUITY])
#
# db_ru_mentioned = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_RU_MENTIONED_BUT_NOT_USED])
# db_ru_hetero = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_RU_HETERO_AMBIGUITY])
# db_ru_tables = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_RU_TABLES_AMBIGUITY])
# db_ru_columns = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_RU_COLUMNS_AMBIGUITY])
# db_ru_values = araneae.find_all_with_type(QueryType.DB, subtypes=[QuerySubtype.DB_RU_VALUES_AMBIGUITY])
#
# save({
#     "db_en_mentioned": db_en_mentioned,
#     "db_en_hetero": db_en_hetero,
#     "db_en_tables": db_en_tables,
#     "db_en_columns": db_en_columns,
#     "db_en_values": db_en_values,
#     "db_ru_mentioned": db_ru_mentioned,
#     "db_ru_hetero": db_ru_hetero,
#     "db_ru_tables": db_ru_tables,
#     "db_ru_columns": db_ru_columns,
#     "db_ru_values": db_ru_values
# })

# #########################################################################################
# # BINARY
# binary_pipeline = [QueryType.BINARY]
# araneae.add_specifications(binary_pipeline)
#
# binary_with_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITH_VALUES])
# binary_without_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITHOUT_VALUES])
#
# save({
#     "binary_with_values": binary_with_values,
#     "binary_without_values": binary_without_values
# })

#########################################################################################
# DATETIME
# datetime_pipeline = [QueryType.DATETIME]
# araneae.add_specifications(datetime_pipeline)
#
# datetimes_with_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITH_VALUES])
# datetimes_without_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITHOUT_VALUES])
#
# save({
#     "datetimes_with_values": datetimes_with_values,
#     "datetimes_without_values": datetimes_without_values
# })


#########################################################################################
# SIMPLICITY
# simplicity_pipeline = [QueryType.SIMPLICITY]
# araneae.add_specifications(simplicity_pipeline)
#
# extra_simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.EXTRA_SIMPLE])
# simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.SIMPLE])
#
# save({
#     "extra_simple": extra_simple,
#     "simple": simple
# })


########################################################################################
# # SQL - skeleton
# sql_skeleton_pipeline = [QueryType.JOIN, QueryType.SELECT]
# araneae.add_specifications(sql_skeleton_pipeline)
#
# single_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.SINGLE_JOIN])
# multi_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.MULTI_JOIN])
# multi_select = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MULTI_SELECT])
# mono_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MONO_AGG])
# hetero_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.HETERO_AGG])
#
# save({
#     "single_join": single_join,
#     "multi_join": multi_join,
#     "multi_select": multi_select,
#     "mono_agg": mono_agg,
#     "hetero_agg": hetero_agg
# })

########################################################################################
# # SQL - temporary
# sql_temporary_pipeline = [QueryType.SQL, QueryType.WHERE, QueryType.GROUP_BY, QueryType.ORDER_BY]
# araneae.add_specifications(sql_temporary_pipeline)
#
# sql_like = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_LIKE])
# sql_limit = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_LIMIT])
# sql_cast = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_CAST])
# sql_having = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_HAVING])
# sql_between = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_BETWEEN])
# sql_compare = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_COMPARE])
# sql_null = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_NULL])
# sql_except = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_EXCEPT])
# sql_distinct = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_DISCTINCT])
# sql_exists = araneae.find_all_with_type(QueryType.SQL, subtypes=[QuerySubtype.SQL_EXISTS])
#
# where_mono = araneae.find_all_with_type(QueryType.WHERE, subtypes=[QuerySubtype.WHERE_MONO])
# where_multi = araneae.find_all_with_type(QueryType.WHERE, subtypes=[QuerySubtype.WHERE_MULTI])
#
# group_by_exists = araneae.find_all_with_type(QueryType.GROUP_BY, subtypes=[QuerySubtype.GROUP_BY_EXISTS])
# group_by_count = araneae.find_all_with_type(QueryType.GROUP_BY, subtypes=[QuerySubtype.GROUP_BY_COUNT])
#
# order_by_exists = araneae.find_all_with_type(QueryType.ORDER_BY, subtypes=[QuerySubtype.ORDER_BY_EXISTS])
# order_by_count = araneae.find_all_with_type(QueryType.ORDER_BY, subtypes=[QuerySubtype.ORDER_BY_COUNT])
#
# save({
#     "sql_like": sql_like,
#     "sql_limit": sql_limit,
#     "sql_cast": sql_cast,
#     "sql_having": sql_having,
#     "sql_between": sql_between,
#     "sql_compare": sql_compare,
#     "sql_null": sql_null,
#     "sql_except": sql_except,
#     "sql_distinct": sql_distinct,
#     "sql_exists": sql_exists,
#     "where_mono": where_mono,
#     "where_multi": where_multi,
#     "group_by_exists": group_by_exists,
#     "group_by_count": group_by_count,
#     "order_by_exists": order_by_exists,
#     "order_by_count": order_by_count
# })

# ########################################################################################
# # NL
# nl_pipeline = [QueryType.NL]
# araneae.add_specifications(nl_pipeline)
#
# nl_several_sentences = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SEVERAL_SENTENCES])
# nl_short_sql_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SHORT_SQL_LONG])
# nl_long_sql_short = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG_SQL_SHORT])
# nl_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG])
#
# save({
#     "nl_several_sentences": nl_several_sentences,
#     "nl_short_sql_long": nl_short_sql_long,
#     "nl_long_sql_short": nl_long_sql_short,
#     "nl_long": nl_long
# })
#
# #########################################################################################
# # LOGIC
# logic_pipeline = [QueryType.LOGIC, QueryType.NEGATION]
# araneae.add_specifications(logic_pipeline)
#
# logic_vice_versa = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_VS])
# logic_all_nl_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL, QuerySubtype.LOGIC_NL_ALL])
# logic_andor_nl_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_AND_OR, QuerySubtype.LOGIC_NL_AND_OR_OR])
# logic_sql = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL])
# logic_and_with_or_nl = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_NL_AND_AND_OR])
# logic_set_phrase = araneae.find_all_with_type(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SET_PHRASE])
# negation = araneae.find_all_with_type(QueryType.NEGATION)
# negation_any_all = araneae.find_all_with_type(QueryType.NEGATION, subtypes=[QuerySubtype.NEGATION_ANY_ALL])
#
# save({
#     "logic_vice_versa": logic_vice_versa,
#     "logic_all_nl_sql": logic_all_nl_sql,
#     "logic_andor_nl_sql": logic_andor_nl_sql,
#     "logic_sql": logic_sql,
#     "logic_and_with_or_nl": logic_and_with_or_nl,
#     "logic_set_phrase": logic_set_phrase,
#     "negation": negation,
#     "negation_any_all": negation_any_all
# })




