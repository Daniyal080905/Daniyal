import re
a = str(input())
x = re.findall("cat|dog",a)
if x:
    print("Yes")
else:
    print("No")