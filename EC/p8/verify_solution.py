def f(x):
    return ((((x+ (x* x)) * x) + x) * x) + x


points=[x/10. for x in range(-10, 11)]

for x in points:
    y = f(x)
    print(f'f({x}) : {y}')
