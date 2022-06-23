from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#
# NEW
db_pipeline = [QueryType.NEW]
araneae.add_specifications(db_pipeline)

new_all = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_ALL])
empty = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_EMPTY])
long = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_LONG])
new_binary = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_BINARY])
new_fuzzy = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_FUZZY])
new_dates = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.NEW_DATES])

save({
    "service_new_all": new_all,
    "final_empty": empty,
    "final_long": long,
    "service_new_binary": new_binary,
    "service_new_fuzzy": new_fuzzy,
    "service_new_dates": new_dates
})

araneae.save()

