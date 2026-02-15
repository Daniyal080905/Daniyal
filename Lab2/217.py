n = int(input())

freq = {}  

for _ in range(n):
    phone = input().strip()
    freq[phone] = freq.get(phone, 0) + 1

count = 0
for x in freq:
    if freq[x] == 3:
        count += 1

print(count)