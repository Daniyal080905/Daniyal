import re

a = input()

if re.match(r"Hello", a):
    print("Yes")
else:
    print("No")