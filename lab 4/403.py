a = int(input())
for i in range(0, a+1):
    if i%3==0 and i%4==0 or i==0:
        print(i, end = " ")