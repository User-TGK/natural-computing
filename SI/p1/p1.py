import math
x0 = [-420.9687, -420.9687]
x1 = [-400, -400]
x2 = [-410, -410]
x3 = [-415, -415]

def f (xs):
    return sum([(-xs[i]) * math.sin(math.sqrt(abs(xs[i]))) for i in range(2)])

print(f(x0))
print(f(x1))
print(f(x2))
print(f(x3))


def personal_best(x):
    return x

def global_best(i):
    return x3[i]


velocity = [(-50,-50),(-50,-50),(-50,-50)]
alpha1 = alpha2 = 1
radius1 = radius2 = 0.5

x = [x1,x2,x3]

def update(j,omega):
    return [omega*velocity[j][i] + alpha1*radius1*(personal_best(x[j][i]) - x[j][i]) + alpha1*radius2*(global_best(i) - x[j][i]) for i in range (2)]

def g(j, omega):
    xs = [ x[j][i] + update(j,omega)[i] for i in range(len((update(j,omega)))) if x[j][i] + update(j,omega)[i] ]
    return list(map(lambda x: clamp(x, -500, 500), xs))

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
    

print(g(0,2))
print(g(1,2))
print(g(2,2))

print(g(0,0.5))
print(g(1,0.5))
print(g(2,0.5))

print(g(0,0.1))
print(g(1,0.1))
print(g(2,0.1))