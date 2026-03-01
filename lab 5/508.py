import re

a = input()
b = input()

x = re.split(b, a)

print(",".join(x))