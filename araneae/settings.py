#  Conditions, renaming, condition, calendar-functions are collapsing

KEY_WORDS = [
    "select",
    "from",
    "where",
    "join",
    "by",
    "order",
    "group",
    "desc",
    "asc",
    "intersect",
    "union",
    "having",
    "limit",
    "in",
    "except",
    # "hour",
    # "second",
    # "minute",
    # "year",
    # "month",
    # "type,
    ","
]
AGGREGATIONS = [
    "min",
    "max",
    "avg",
    "sum",
    "count",
    "between",
    "*", "*",
    "distinct",
    "cast",
    "length",
    "and",
    "or", 'or',
    "not",
    "like",
    "not",
    "(",
    ")"
]
OTHER_KEYWORDS = {
    "as",
    "on"
}

SQL_NL_THRESHOLD = 5.
NL_SQL_THRESHOLD = 2.
LONG_NL = 30