import re

a = input()

x = re.search(r"\S+@\S+\.\S+", a)

if x:
    print(x.group())
else:
    print("No email")