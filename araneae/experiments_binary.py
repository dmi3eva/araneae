from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

# BINARY
binary_pipeline = [QueryType.TWO]
araneae.add_specifications(binary_pipeline)


two_values_without_values = araneae.find_all_with_type_and(QueryType.TWO, subtypes=[QuerySubtype.WITHOUT_VALUES])
binary_all = araneae.find_all_with_type_and(QueryType.TWO, subtypes=[QuerySubtype.WITH_VALUES, QuerySubtype.JUST_BINARY])
gender_all = araneae.find_all_with_type_and(QueryType.TWO, subtypes=[QuerySubtype.WITH_VALUES, QuerySubtype.TWO_GENDER])
antonyms_all = araneae.find_all_with_type_and(QueryType.TWO, subtypes=[QuerySubtype.WITH_VALUES, QuerySubtype.TWO_ANTONYMS])
two_values_new = araneae.find_all_with_type_and(QueryType.NEW, subtypes=[QuerySubtype.WITH_VALUES, QuerySubtype.NEW_BINARY])
binary_old = araneae.find_all_with_type_and(QueryType.TWO, subtypes=[QuerySubtype.WITH_VALUES, QuerySubtype.JUST_BINARY_OLD])


save({
    "final_binary": binary_all,
    "final_gender": gender_all,
    "final_antonyms": antonyms_all,
    "service_two_values_without_values": two_values_without_values,
    "service_two_values_new": two_values_new,
    "service_binary_old": binary_old,
})

araneae.save()