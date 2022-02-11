import random

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

def total_distance(xs):
    distances = [ distance(xs[i], xs[hack(i+1, xs)]) for i in range(len(xs))] 
    return sum(distances)

def fitness(xs):
    total_distance_traveled = total_distance(xs)
    fitness = 1 / total_distance_traveled
    return fitness

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
   result = []
   result.extend(parent)
   xs_left = result[:cutpoint_start]
   xs_right = result[cutpoint_end-len(result):]
   xs.extend(xs_left)
   xs.extend(xs_right)
   xs = mutate(xs, 0.1)
   m_i = 0
   for i in range(len(result)):
        if (i < cutpoint_start or i >= cutpoint_end):
            result[i] = xs[m_i]
            m_i = m_i + 1
   return result


def es(parent, offspring):
    if(fitness(parent) < fitness(offspring)):
        parent = offspring
    return parent

def _2optSwap(existing_route, i, k):
   new_route = []
   left_route = []
   left_route.extend(existing_route[:i+1])
   center_route = []
   center_route.extend(existing_route[i+1:k+1])
   center_route.reverse()
   right_route = []
   right_route.extend(existing_route[k+1:])
   new_route.extend(left_route)
   new_route.extend(center_route)
   new_route.extend(right_route)
   return new_route

def tsp_ma(coords, iterations):
    counter = 0
    existing_route = []
    existing_route.extend(coords)
    best_distance = total_distance(existing_route)
    while counter < iterations:
        counter += 1
        for i in range(len(existing_route)-2):
            for k in range(i+2, len(existing_route)-1):
                new_route = _2optSwap(existing_route, i, k) 
                new_distance = total_distance(new_route)
                if new_distance < best_distance:
                    existing_route = new_route
                    best_distance = new_distance
    return existing_route

def tsp_ea(coords, iterations):
    # cutpoint_start = 1, cutpoint_end = 2
    # [(a,b), (c,d), (e,f), (g,h)]
    #  ^^^^^  ^^^^^  ^^^^^  ^^^^^
    #  0      1      2      3
    #         ^^^^^^^^^^^^
    # permutate on [(a,b), (g,h)]
    # crossover() can return both
    # [(g,h), (c,d), (e,f), (a,b)]
    # [(a,b), (c,d), (e,f), (g,h)]
    
    counter = 0
    parent = []
    parent.extend(coords)
    
    while counter < iterations:
        counter += 1
        z = random.randint(0, len(parent)-2)
        w = random.randint(z, len(parent)-1)
        offspring = crossover(z,w, parent)
        offspring = mutate(offspring, 0.1)
        parent = es(parent, offspring) # (1 + 1)-ES
               
    return parent

def main():
    coords = []
    file_in = open('file-tsp.txt', 'r')
    for y in file_in.read().split('\n'):
        w = y.split()
        coords.append([float(i) for i in w])
    result_ea = tsp_ea(coords,1500)
    result_ma = tsp_ma(coords,1500)
    
    # coords = [[0,0], [10,10], [40,40], [20,20], [30,30]] # sanity check should result 160 instead of 200
    
    print("Init: ", repr(total_distance(coords)))
    print("EA: ", repr(total_distance(result_ea)))
    print("MA: ", repr(total_distance(result_ma)))
main()
