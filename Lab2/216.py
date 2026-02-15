a = int(input())
arr = list(map(int, input().split()))
v = set()
for i in arr:
    if i not in v:
        print("YES")
        v.add(i)
    else:
        print("NO")
        