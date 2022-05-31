template = """"
Test {a} test {b}
"""

value_1 = template.format(a="1", b="2")
print(value_1)
value_2 = template.format(a="1", b="2", c="2")
print(value_2)
# value_3 = template.format(a="1")
# print(value_3)