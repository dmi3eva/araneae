from araneae.experiments import *


araneae = Araneae()
araneae.load()

# #######################################################
# ############  Experiments   ##############################
# #######################################################
#

########################################################################################

# #########################################################################################
# SQL - temporary
sql_temporary_pipeline = [QueryType.SQL, QueryType.WHERE, QueryType.GROUP_BY, QueryType.ORDER_BY]
araneae.add_specifications(sql_temporary_pipeline)

sql_like = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_LIKE])
sql_limit = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_LIMIT])
sql_cast = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_CAST])
sql_having = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_HAVING])
sql_between = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_BETWEEN])
sql_compare = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_COMPARE])
sql_null = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_NULL])
sql_except = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_EXCEPT])
sql_distinct = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_DISCTINCT])
sql_exists = araneae.find_all_with_type_and(QueryType.SQL, subtypes=[QuerySubtype.SQL_EXISTS])

where_mono = araneae.find_all_with_type_and(QueryType.WHERE, subtypes=[QuerySubtype.WHERE_MONO])
where_multi = araneae.find_all_with_type_and(QueryType.WHERE, subtypes=[QuerySubtype.WHERE_MULTI])

group_by_exists = araneae.find_all_with_type_and(QueryType.GROUP_BY, subtypes=[QuerySubtype.GROUP_BY_EXISTS])
group_by_count = araneae.find_all_with_type_and(QueryType.GROUP_BY, subtypes=[QuerySubtype.GROUP_BY_COUNT])

order_by_exists = araneae.find_all_with_type_and(QueryType.ORDER_BY, subtypes=[QuerySubtype.ORDER_BY_EXISTS])
order_by_count = araneae.find_all_with_type_and(QueryType.ORDER_BY, subtypes=[QuerySubtype.ORDER_BY_COUNT])

save({
    "sql_like": sql_like,
    "sql_limit": sql_limit,
    "sql_cast": sql_cast,
    "sql_having": sql_having,
    "sql_between": sql_between,
    "sql_compare": sql_compare,
    "sql_null": sql_null,
    "sql_except": sql_except,
    "sql_distinct": sql_distinct,
    "sql_exists": sql_exists,
    "where_mono": where_mono,
    "where_multi": where_multi,
    "group_by_exists": group_by_exists,
    "group_by_count": group_by_count,
    "order_by_exists": order_by_exists,
    "order_by_count": order_by_count
})

araneae.save()