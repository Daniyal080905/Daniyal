a = int(input())
arr = list(map(int, input().split()))
sum = 0
for i in arr:
    if i>0:
        sum+=1
        
print(sum)