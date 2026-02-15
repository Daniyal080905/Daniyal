n = int(input())
arr = []

for _ in range(n):
    arr.append(input())

first_index = {}

for i in range(n):
    if arr[i] not in first_index:
        first_index[arr[i]] = i + 1

for s in sorted(first_index):
    print(s, first_index[s])
