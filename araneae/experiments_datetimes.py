from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

########################################################################################
# DATETIME
datetime_pipeline = [QueryType.DATETIME]
araneae.add_specifications(datetime_pipeline)

datetimes_with_values = araneae.find_all_with_type_and(QueryType.DATETIME, subtypes=[QuerySubtype.WITH_VALUES])
datetimes_without_values = araneae.find_all_with_type_and(QueryType.DATETIME, subtypes=[QuerySubtype.WITHOUT_VALUES])

save({
    "final_datetimes_with_values": datetimes_with_values,
    "service_datetimes_without_values": datetimes_without_values
})

araneae.save()