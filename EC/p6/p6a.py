import itertools
import random



# Fitness function is (1 / distance function)
# Representation is a permutated list of coords of each city
# TODO: Crossover, mutation for 6a this is a simple EA algorithm so we choose (1+1)-EC
# 

coords = [[1,2], [3,4], [2,3], [4,4], (7,7), (10,5), (4,2)]
goal = 1
def distance (src, dest):
   x = abs(src[0] - dest[0])
   y = abs(src[1] - dest[1])
   return abs(x + y)

def hack(x):
    if x >= len(coords): #to make the round trip
        return 0
    else: 
        return x

def print_path( xs ):
    return [ f"{x} -> " for x in xs ]

def fitness(xs):
    distances = [ distance(xs[i], xs[hack(i+1)]) for i in range(len(xs))] 
    total_distance_traveled = sum(distances)
    fitness = 1 / total_distance_traveled
    return fitness

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def crossover(cutpoint_start, cutpoint_end, parent1, parent2):
    parent1_schema = [ x for i, x in enumerate(parent1) if i < cutpoint_start or i > cutpoint_end]
    parent2_schema = [ x for i, x in enumerate(parent2) if i < cutpoint_start or i > cutpoint_end]
    k1 = []
    k2 = []
    k1.extend(parent1_schema)
    k2.extend(parent2_schema) # create list of possible mutation crossover
    new_k1 = []
    new_k2 = []
    for elem in k1: # remove dups
        if elem not in new_k1:
           new_k1.append(elem)
    for elem in k2: # remove dups
        if elem not in new_k2:
           new_k2.append(elem)
    perms1 = list(itertools.permutations(new_k1))
    perms2 = list(itertools.permutations(new_k2))
    offspring1 = list(parent1)
    offspring2 = list(parent2)
    mutation_counter = cutpoint_end - cutpoint_start - 1
    x = random.randint(0, len(new_k1)-1) # random permutation selection
    y = random.randint(0, len(new_k2)-1) # random permuation selection
    print(repr(parent1_schema))
    for i in range(len(offspring1)):
        if i < cutpoint_start or i > cutpoint_end:
            if list(perms1[x][mutation_counter]) not in intersection(offspring1, parent1_schema): 
               offspring1[i] = list(perms1[x])[mutation_counter]
            if list(perms2[y][mutation_counter]) not in intersection(offspring2, parent2_schema): 
               offspring2[i] = list(perms2[y])[mutation_counter]
            mutation_counter = mutation_counter - 1
    return offspring1, offspring2


def ea(parent, offspring):
    if(fitness(parent) < fitness(offspring)):
      parent = offspring 
    return parent

def print_info(parent1, parent2, fst, snd):
    print("parent:")
    print(print_path(parent1))
    print(fitness(parent1))
    print("offspring")
    print(print_path(fst))
    print(fitness(fst))
    print("parent2:")
    print(print_path(parent2))
    print(fitness(parent2))
    print("offspring2:")
    print(print_path(snd))
    print(fitness(snd))
    

def tsp():
    perms = list(itertools.permutations(coords))
    # cutpoint_start = 1, cutpoint_end = 2
    # [(a,b), (c,d), (e,f), (g,h)]
    #  ^^^^^  ^^^^^  ^^^^^  ^^^^^
    #  0      1      2      3
    #         ^^^^^^^^^^^^
    # permutate on [(a,b), (g,h)]
    # crossover() can return both
    # [(g,h), (c,d), (e,f), (a,b)]
    # [(a,b), (c,d), (e,f), (g,h)]
 
    cutpoint_start = 1
    cutpoint_end = 2
    parent1 = perms[0]
    parent2 = perms[1]
    
    count = 5

    fst, snd = crossover(cutpoint_start, cutpoint_end, perms[0], perms[1]) 
    while(count > 0):
        count = count - 1
        print_info(parent1,parent2, fst, snd)
        fst, snd = crossover(cutpoint_start, cutpoint_end, perms[0], perms[1]) 
        parent1 = fst
        parent2 = snd


tsp()
