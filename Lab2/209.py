a = int(input())
arr = list(map(int, input().split()))
max_num = max(arr)  
min_num = min(arr)
for i in range(a):
    if arr[i] == max_num:
        arr[i] = min_num

print(*arr)