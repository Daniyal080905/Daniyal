a = int(input())
arr = list(map(int, input().split()))
max = arr[0]
pos = 1
for i in range(a):
    if max<arr[i]:
        max=arr[i]
        pos = i+1
        
print(pos)
    
