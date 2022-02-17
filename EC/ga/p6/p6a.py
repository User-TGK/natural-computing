import random
import matplotlib.pyplot as plt

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
    existing_route = []
    intermediate_results = []
    existing_route.extend(coords)
    best_distance = total_distance(existing_route)
    for _ in range(iterations):
        intermediate_results.append(best_distance)
        for i in range(len(existing_route)-2):
            for k in range(i+2, len(existing_route)-1):
                new_route = _2optSwap(existing_route, i, k) 
                new_distance = total_distance(new_route)
                if new_distance < best_distance:
                    existing_route = new_route
                    best_distance = new_distance
    return existing_route, intermediate_results

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
    
    parent = []
    parent.extend(coords)
    intermediate_results = []
    
    for _ in range(iterations):
        z = random.randint(0, len(parent)-2)
        w = random.randint(z, len(parent)-1)
        offspring = crossover(z,w, parent)
        offspring = mutate(offspring, 0.1)
        parent = es(parent, offspring) # (1 + 1)-ES
        intermediate_results.append(total_distance(parent))
    
    return parent, intermediate_results

def sanity_check():
    coords = [[0,0], [10,10], [40,40], [20,20], [30,30]] # sanity check should result 160 instead of 200
    result_ea, _ = tsp_ea(coords,1500)
    result_ma, _ = tsp_ma(coords,1500)
    assert(total_distance(result_ea) == 160)
    assert(total_distance(result_ma) == 160)
    assert(total_distance(coords) == 200)

def load_file(fp):
    coords = []
    file_in = open(fp, 'r')
    for y in file_in.read().split('\n'):
        w = y.split()
        coords.append([float(i) for i in w])
    return coords

def main():
    sanity_check()
    # coords = load_file('file-tsp.txt')
    coords = load_file('burma14.txt')
    runs = 10
    iterations = 1500
    _fig, ax = plt.subplots()
    for run in range(runs):
        coords = mutate(coords,1) # randomize inital ordering of positions of city
        result_ea, intermediate_result_ea = tsp_ea(coords,iterations)
        result_ma, intermediate_result_ma = tsp_ma(coords,iterations)
        print("Init: ", repr(total_distance(coords)))
        print("EA: ", repr(total_distance(result_ea)))
        print("MA: ", repr(total_distance(result_ma)))
        
        ax.plot(list(range(1, iterations+1)), intermediate_result_ea, "-b", label="EA {}".format(run))
        ax.plot(list(range(1, iterations+1)), intermediate_result_ma, "-g", label="MA {}".format(run))
        plt.legend()
    
    plt.xlabel('iterations')
    plt.ylabel('total distance')
    plt.show()
        
main()
