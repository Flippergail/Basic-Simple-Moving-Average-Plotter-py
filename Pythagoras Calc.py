import math
def abcalculate(a, b):
    c2 = a**2 + b**2
    c = c2**(1/2)
    return c
def cacalculate(c, a):
    b2 = c**2 - a**2
    b = b2**(1/2)
    return b

a = input("What length is a? ")
b = input("What length is b? ")
c = input("What length is c? ")
if str(a) != "find" and str(b) != "find":
    ans = abcalculate(int(a), int(b))
    print(ans)
elif str(a) != "find" and str(c) != "find":
    ans = cacalculate(int(c), int(a))
    print(ans)
else:
    print("ERROR")