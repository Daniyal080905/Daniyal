import re
a = input()
txt = re.compile(r"\b\w+\b")
r = txt.findall(a)
print(len(r))