import array
import random
from deap import creator, base, tools, algorithms

l = 100
def create_bit_string(l):
    key = ""
    for i in range(l):
        temp = str(random.randint(0, 1))
        key+= temp
        
    return (key)

def mutate(x):
    for i in x:
        x[i] = random.choices([x[i]], (1-(1/l), 1/l), k=2)

ind1 = create_bit_string(l)
toolbox = base.Toolbox()
mutant = toolbox.clone(ind1)
# ind2, = 
# del mutant.fitness.values
# selected = tools.selBest([ind1, ind2], 2)
# print(selected)

