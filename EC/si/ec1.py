import math
def f (xs):
    return sum([(-xs[i]) * math.sin(math.sqrt(abs(xs[i]))) for i in range(2)])

x0 = [-420.9687, -420.9687]
x1 = [-400, -400]
x2 = [-410, -410]
x3 = [-415, -415]

print(f(x0))