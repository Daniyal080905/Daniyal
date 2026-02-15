
a = int(input())
sum = 0
for i in range(1,a + 1):
    if a % i == 0:
        sum += 1
if sum == 2:
    print("Yes")
else:
    print("No")