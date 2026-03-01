import re
a = input()
x = re.findall(r"\d{2,9}",a)
print(*x) 