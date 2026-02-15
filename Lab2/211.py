a, b, c = map(int, input().split())
arr = list(map(int, input().split()))
b-=1
c-=1
arr[b:c+1] = arr[b:c+1][::-1]
print(*arr)
