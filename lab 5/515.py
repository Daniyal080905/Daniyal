import re
a = input()
x = re.sub(r"(\d)", r"\1\1", a)
print (x)