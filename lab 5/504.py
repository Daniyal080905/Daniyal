import re
a = input()
x = re.findall("[0-9]", a)
print(*x)