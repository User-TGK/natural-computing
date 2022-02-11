import itertools
import random

# Fitness function is (1 / distance function)
# Representation is a permutated list of coords of each city
# TODO: Crossover, mutation for 6a this is a simple EA algorithm so we choose (1+1)-EC
# 

def distance (src, dest):
   x = abs(src[0] - dest[0])
   y = abs(src[1] - dest[1])
   return abs(x + y)

def hack(x, coords):
    if x >= len(coords): #to make the round trip
        return 0
    else: 
        return x

def print_path( xs ):
    return [ f"{x} -> " for x in xs ]

def fitness(xs):
    distances = [ distance(xs[i], xs[hack(i+1, xs)]) for i in range(len(xs))] 
    total_distance_traveled = sum(distances)
    fitness = 1 / total_distance_traveled
    return fitness

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def mutate(xs, chance):
    for i in range(len(xs)):
        if random.random() < chance:
            y = xs[i]
            z = random.randint(0, len(xs)-1)
            w = xs[z]
            xs[i] = w
            xs[z] = y
    return xs

def crossover(cutpoint_start, cutpoint_end, parent):
   xs = []
   xs_left = parent[:cutpoint_start]
   xs_right = parent[cutpoint_end-len(parent):]
   xs.extend(xs_left)
   xs.extend(xs_right)
   xs = mutate(xs, 1)
   m_i = 0
   for i in range(len(parent)):
        if (i < cutpoint_start or i >= cutpoint_end):
            parent[i] = xs[m_i]
            m_i = m_i + 1
   return parent


def ea(parent, offspring):
    if(fitness(parent) < fitness(offspring)):
      parent = offspring 
    return parent

def tsp(coords):
    # cutpoint_start = 1, cutpoint_end = 2
    # [(a,b), (c,d), (e,f), (g,h)]
    #  ^^^^^  ^^^^^  ^^^^^  ^^^^^
    #  0      1      2      3
    #         ^^^^^^^^^^^^
    # permutate on [(a,b), (g,h)]
    # crossover() can return both
    # [(g,h), (c,d), (e,f), (a,b)]
    # [(a,b), (c,d), (e,f), (g,h)]
    pass

def main():
    coords = []
    file_in = open('file-tsp.txt', 'r')
    for y in file_in.read().split('\n'):
        w = y.split()
        # print(repr(w))
        coords.append([float(i) for i in w])

    # coords = [[int(i), int(j)] for [i,j] in coords]  # <- TODO: fix for file
    # print(repr(coords))
    # coords = [[1,2], [4,3], [5,6], [8,8]]
    # coords = [[1,2], [4,3], [5,6], [8,8], [5,6], [4,1], [2,2]]
    # coords = [[0, 18], [0, 15], [0, 8], [1, 16], [1, 17], [2, 9], [6, 7], [7, 0], [7, 13], [8, 5]] # really slow <- from on here
    print(repr(coords))
    print(repr(crossover(1,3,coords)))
    # tsp(coords)

main()
