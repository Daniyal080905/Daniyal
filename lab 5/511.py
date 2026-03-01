import re
a = str(input())
x = re.findall("[A-Z]", a)
print(len(x))