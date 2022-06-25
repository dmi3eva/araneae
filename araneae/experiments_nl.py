from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

# #########################################################################################
# NL
nl_pipeline = [QueryType.NL]
araneae.add_specifications(nl_pipeline)

nl_several_sentences = araneae.find_all_with_type_and(QueryType.NL, subtypes=[QuerySubtype.NL_SEVERAL_SENTENCES])
nl_short_sql_long = araneae.find_all_with_type_and(QueryType.NL, subtypes=[QuerySubtype.NL_SHORT_SQL_LONG])
nl_long_sql_short = araneae.find_all_with_type_and(QueryType.NL, subtypes=[QuerySubtype.NL_LONG_SQL_SHORT])
nl_long = araneae.find_all_with_type_and(QueryType.NL, subtypes=[QuerySubtype.NL_LONG])

save({
    "nl_several_sentences": nl_several_sentences,
    "nl_short_sql_long": nl_short_sql_long,
    "nl_long_sql_short": nl_long_sql_short,
    "nl_long": nl_long
})


araneae.save()