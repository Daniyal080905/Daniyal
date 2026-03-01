import re
a = input()
b = input()
c= re.escape(b)

x =re.findall(c,a) 
print(len(x))