import re
a = input()
x = re.compile(r"^\d+$")
if x.fullmatch(a):
    print("Match")
else:
    print("No match")