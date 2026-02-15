a = int(input())
names = set()
for _ in  range(a):
    name = input().strip()
    names.add(name)
    
print(len(names))