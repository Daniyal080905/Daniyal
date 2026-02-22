def number(a):
    for i in str(abs(a)):
        if int(i) % 2 != 0:
            return "Not valid"
    return "Valid"

a = int(input())
print(number(a))
