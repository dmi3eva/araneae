from dto.sample import *

triples = [
    Triple("a", "b", "c"),
    Triple("a", "d", "e")
]

positive = Triple("a", "b", "c")
negative = Triple("a", "d", "f")

print(positive in triples)
print(negative in triples)