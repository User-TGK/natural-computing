import itertools



# Fitness function is (1 / distance function)
# Representation is a permutated list of coords of each city
# TODO: Crossover, mutation for 6a this is a simple EA algorithm so we choose (1+1)-EC
# 

coords = [[1,2], [3,4], [2,3], [4,4]]
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
 
def crossover(cutpoint_start, cutpoint_end, parent1, parent2):
    parent1_schema = [ x for i, x in enumerate(parent1) if i < cutpoint_start or i > cutpoint_end]
    parent2_schema = [ x for i, x in enumerate(parent2) if i < cutpoint_start or i > cutpoint_end]
    parent1_schema.extend(parent2_schema) # create list of possible mutation crossover
    new_k = []
    for elem in parent1_schema: # remove dups
        if elem not in new_k:
           new_k.append(elem)
    perms = list(itertools.permutations(new_k))
    offspring1 = list(parent1)
    offspring2 = list(parent2)
    for i in range(len(offspring1)):
        if i < cutpoint_start or i > cutpoint_end:
            offspring1[i] = list(perms[0])[0]
            offspring2[i] = list(perms[1])[1]
    return offspring1, offspring2


#def ea(parent1, parent2, step):
#    if step > 10: return parent1, parent2
#    offspring1, offspring2 = crossover(parent1, parent2)
#    ea(offspring1, offspring2)
#    if fitness(parent1) >= goal: return parent1, parent2 
#    if fitness(parent2) >= goal: return parent2, parent1

def tsp():
    perms = list(itertools.permutations(coords))
    
    cutpoint_start = 1
    cutpoint_end = 2
    fst, snd = crossover(cutpoint_start, cutpoint_end, perms[0], perms[1]) 
    print("parent:")
    print(print_path(perms[0]))
    print("offspring")
    print(print_path(fst))
    print("parent2:")
    print(print_path(perms[1]))
    print("offspring2:")
    print(print_path(snd))
    
       


tsp()
