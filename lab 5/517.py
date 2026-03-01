import re
a = input()
txt = r"((\d{2})/(\d{2})/(\d{4}))"
x = re.findall(txt,a)
print(len(x))