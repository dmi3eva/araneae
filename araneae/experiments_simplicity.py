from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

# SIMPLICITY
simplicity_pipeline = [QueryType.SIMPLICITY]
araneae.add_specifications(simplicity_pipeline)

extra_simple = araneae.find_all_with_type_and(QueryType.SIMPLICITY, subtypes=[QuerySubtype.EXTRA_SIMPLE])
simple = araneae.find_all_with_type_and(QueryType.SIMPLICITY, subtypes=[QuerySubtype.SIMPLE])

save({
    "extra_simple": extra_simple,
    "simple": simple
})

araneae.save()
