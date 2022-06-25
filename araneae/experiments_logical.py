from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

# #########################################################################################
# LOGIC
logic_pipeline = [QueryType.LOGIC, QueryType.NEGATION]
araneae.add_specifications(logic_pipeline)

logic_vice_versa = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_VS])
logic_all_nl_sql = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL, QuerySubtype.LOGIC_NL_ALL])
logic_andor_nl_sql = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_AND_OR, QuerySubtype.LOGIC_NL_AND_OR_OR])
logic_sql = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SQL_ALL])
logic_and_with_or_nl = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_NL_AND_AND_OR])
logic_set_phrase = araneae.find_all_with_type_and(QueryType.LOGIC, subtypes=[QuerySubtype.LOGIC_SET_PHRASE])
negation = araneae.find_all_with_type_and(QueryType.NEGATION)
negation_any_all = araneae.find_all_with_type_and(QueryType.NEGATION, subtypes=[QuerySubtype.NEGATION_ANY_ALL])

save({
    "logic_vice_versa": logic_vice_versa,
    "logic_all_nl_sql": logic_all_nl_sql,
    "logic_andor_nl_sql": logic_andor_nl_sql,
    "logic_sql": logic_sql,
    "logic_and_with_or_nl": logic_and_with_or_nl,
    "logic_set_phrase": logic_set_phrase,
    "negation": negation,
    "negation_any_all": negation_any_all
})


araneae.save()