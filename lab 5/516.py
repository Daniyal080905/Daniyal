import re
a = input()
txt = r"Name: (.+), Age: (.+)"
z = re.search(txt, a)
if z:
    print(z.group(1), z.group(2))