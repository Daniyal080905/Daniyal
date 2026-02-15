n = int(input())
doc = {}

for _ in range(n):
    parts = input().split()
    if parts[0] == "set":
        doc[parts[1]] = parts[2]
    elif parts[0] == "get":
        key = parts[1]
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")
