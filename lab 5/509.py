import re
a = str(input())

x = re.findall(r"\b\w{3}\b", a)

print(len(x))