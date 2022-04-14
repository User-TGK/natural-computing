import math

def calc(n,k):
    sum = 0
    for x in range(k, n):
        sum += math.comb(n,x) * (x/11 * 0.8 * pow(0.6,x-1) * pow((1-0.6),n-x) + (1-x/11) * (1-0.8) * pow((1-0.6),n-x-1) * pow(0.6,x))
    return sum

print(calc(11,6)) //0.78879246336
