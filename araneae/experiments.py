from wrapper import *

TEST_SET_PATH_CSV = '../resources/results/test_sets/csv'
TEST_SET_PATH_JSON = '../resources/results/test_sets/json'
SUBTYPES_PATH_CSV = '../resources/results/subtypes'

########################################################
#############  Starting   ##############################
########################################################

# First start
# araneae = Araneae()
# araneae.import_spider()
# araneae.import_russocampus()


# Other starts
araneae = Araneae()
araneae.load()

########################################################
#############  Experiments   ##############################
########################################################


#########################################################################################
# BINARY
# binary_pipeline = [QueryType.BINARY]
# araneae.add_specifications(binary_pipeline)
#
# binary_with_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITH_VALUES])
# binary_without_values = araneae.find_all_with_type(QueryType.BINARY, subtypes=[QuerySubtype.WITHOUT_VALUES])
#
# binary_with_values.save_in_csv(f'{test_set_path_csv}/binary_with_values.csv')
# binary_without_values.save_in_csv(f'{test_set_path_csv}/binary_without_values.csv')
#
# binary_with_values.save_in_json(f'{test_set_path_json}/binary_with_values.json')
# binary_without_values.save_in_json(f'{test_set_path_json}/binary_without_values.json')

#########################################################################################
# DATETIME
# datetime_pipeline = [QueryType.DATETIME]
# araneae.add_specifications(datetime_pipeline)
#
# datetimes_with_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITH_VALUES])
# datetimes_without_values = araneae.find_all_with_type(QueryType.DATETIME, subtypes=[QuerySubtype.WITHOUT_VALUES])
#
# datetimes_with_values.save_in_csv(f'{test_set_path_csv}/datetimes_with_values.csv')#
# datetimes_without_values.save_in_csv(f'{test_set_path_csv}/datetimes_without_values.csv')
#
# datetimes_with_values.save_in_json(f'{test_set_path_json}/datetimes_with_values.json')
# datetimes_without_values.save_in_json(f'{test_set_path_json}/datetimes_without_values.json')


#########################################################################################
# SIMPLICITY
# simplicity_pipeline = [QueryType.SIMPLICITY]
# araneae.add_specifications(simplicity_pipeline)
#
# extra_simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.EXTRA_SIMPLE])
# simple = araneae.find_all_with_type(QueryType.SIMPLICITY, subtypes=[QuerySubtype.SIMPLE])
#
# extra_simple.save_in_csv(f'{test_set_path_csv}/extra_simple.csv')
# simple.save_in_csv(f'{test_set_path_csv}/simple.csv')
#
# extra_simple.save_in_json(f'{test_set_path_json}/extra_simple.json')
# simple.save_in_json(f'{test_set_path_json}/simple.json')


#########################################################################################
# SQL
# sql_pipeline = [QueryType.JOIN, QueryType.SELECT]
# araneae.add_specifications(sql_pipeline)
#
# single_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.SINGLE_JOIN])
# multi_join = araneae.find_all_with_type(QueryType.JOIN, subtypes=[QuerySubtype.MULTI_JOIN])
# multi_select = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MULTI_SELECT])
# mono_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.MONO_AGG])
# hetero_agg = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.HETERO_AGG])
# nested = araneae.find_all_with_type(QueryType.SELECT, subtypes=[QuerySubtype.NESTED])
#
# single_join.save_in_csv(f'{test_set_path_csv}/single_join.csv')
# multi_join.save_in_csv(f'{test_set_path_csv}/multi_join.csv')
# multi_select.save_in_csv(f'{test_set_path_csv}/multi_select.csv')
# mono_agg.save_in_csv(f'{test_set_path_csv}/mono_agg.csv')
# hetero_agg.save_in_csv(f'{test_set_path_csv}/hetero_agg.csv')
# nested.save_in_csv(f'{test_set_path_csv}/nested.csv')
#
# single_join.save_in_json(f'{test_set_path_json}/single_join.json')
# multi_join.save_in_json(f'{test_set_path_json}/multi_join.json')
# multi_select.save_in_json(f'{test_set_path_json}/multi_select.json')
# mono_agg.save_in_json(f'{test_set_path_json}/mono_agg.json')
# hetero_agg.save_in_json(f'{test_set_path_json}/hetero_agg.json')
# nested.save_in_json(f'{test_set_path_json}/nested.json')

#########################################################################################
# NL
# nl_pipeline = [QueryType.NL]
# araneae.add_specifications(nl_pipeline)
#
# nl_several_sentences = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SEVERAL_SENTENCES])
# nl_short_sql_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_SHORT_SQL_LONG])
# nl_long_sql_short = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG_SQL_SHORT])
# nl_long = araneae.find_all_with_type(QueryType.NL, subtypes=[QuerySubtype.NL_LONG])
#
# nl_several_sentences.save_in_csv(f'{test_set_path_csv}/nl_several_sentences.csv')
# nl_short_sql_long.save_in_csv(f'{test_set_path_csv}/nl_short_sql_long.csv')
# nl_long_sql_short.save_in_csv(f'{test_set_path_csv}/nl_long_sql_short.csv')
# nl_long.save_in_csv(f'{test_set_path_csv}/nl_long.csv')
#
# nl_several_sentences.save_in_json(f'{test_set_path_json}/nl_several_sentences.json')
# nl_short_sql_long.save_in_json(f'{test_set_path_json}/nl_short_sql_long.json')
# nl_long_sql_short.save_in_json(f'{test_set_path_json}/nl_long_sql_short.json')
# nl_long.save_in_json(f'{test_set_path_json}/nl_long.json')

#########################################################################################
# LOGIC
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
# logic_vice_versa.save_in_csv(f'{test_set_path_csv}/logic_vice_versa.csv')
# logic_all_nl_sql.save_in_csv(f'{test_set_path_csv}/logic_all_nl_sql.csv')
# logic_andor_nl_sql.save_in_csv(f'{test_set_path_csv}/logic_andor_nl_sql.csv')
# logic_sql.save_in_csv(f'{test_set_path_csv}/logic_sql.csv')
# logic_and_with_or_nl.save_in_csv(f'{test_set_path_csv}/logic_and_with_or_nl.csv')
# logic_set_phrase.save_in_csv(f'{test_set_path_csv}/logic_set_phrase.csv')
# negation.save_in_csv(f'{test_set_path_csv}/negation.csv')
# negation_any_all.save_in_csv(f'{test_set_path_csv}/negation_any_all.csv')
#
# logic_vice_versa.save_in_json(f'{test_set_path_json}/logic_vice_versa.json')
# logic_all_nl_sql.save_in_json(f'{test_set_path_json}/logic_all_nl_sql.json')
# logic_andor_nl_sql.save_in_json(f'{test_set_path_json}/logic_andor_nl_sql.json')
# logic_sql.save_in_json(f'{test_set_path_json}/logic_sql.json')
# logic_and_with_or_nl.save_in_json(f'{test_set_path_json}/logic_and_with_or_nl.json')
# logic_set_phrase.save_in_json(f'{test_set_path_json}/logic_set_phrase.json')
# negation.save_in_json(f'{test_set_path_json}/negation.json')
# negation_any_all.save_in_json(f'{test_set_path_json}/negation_any_all.json')
#
# negation.split_by_subtypes(QueryType.NEGATION, f'{subtypes_path_csv}/negation.csv')
# negation.split_by_subtypes(QueryType.LOGIC, f'{subtypes_path_csv}/logic.csv')
# negation.split_by_subtypes(QueryType.NL, f'{subtypes_path_csv}/nl.csv')
# negation.split_by_subtypes(QueryType.SELECT, f'{subtypes_path_csv}/select.csv')
# negation.split_by_subtypes(QueryType.DATETIME, f'{subtypes_path_csv}/datetime.csv')
# negation.split_by_subtypes(QueryType.BINARY, f'{subtypes_path_csv}/binary.csv')





