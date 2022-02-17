import operator
import math
import matplotlib.pyplot as plt

import numpy

from deap import algorithms
from deap import base
from deap import gp
from deap import creator
from deap import tools

ITERATIONS = 50
CROSSOVER_PROBABILITY = 0.7
MUTATION_PROBABILITY = 0

# Safediv variant
def div(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

# Safelog variant
def log(value):
    try:
        return math.log(value)
    except ValueError:
        return value


pset = gp.PrimitiveSet("MAIN", 1)

pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)

pset.addPrimitive(log, 1)

pset.addPrimitive(math.exp, 1)
pset.addPrimitive(math.sin, 1)
pset.addPrimitive(math.cos, 1)

pset.addPrimitive(div, 2)

pset.renameArguments(ARG0='x')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate,
                 creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

values = {
    -1.0: 0.0000,
    -0.9: -0.1629,
    -0.8: -0.2624,
    -0.7: -0.3129,
    -0.6: -0.3264,
    -0.5: -0.3125,
    -0.4: -0.2784,
    -0.3: -0.2289,
    -0.2: -0.1664,
    -0.1: -0.0909,
    0:  0.000,
    0.1:  0.1111,
    0.2:  0.2496,
    0.3:  0.4251,
    0.4:  0.6496,
    0.5:  0.9375,
    0.6:  1.3056,
    0.7:  1.7731,
    0.8:  2.3616,
    0.9:  3.0951,
    1.0:  4.0000
}

# Fitness evaluation
def eval(individual, points):
    func = toolbox.compile(expr=individual)
    sqerrors = ((func(x) - values[x])**2 for x in points)

    return math.fsum(sqerrors),

toolbox.register("evaluate", eval, points=[x/10. for x in range(-10, 11)])
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", gp.cxOnePoint)

# Compute statistics
def stats(population):
    fitnesses = [ind.fitness.values[0] for ind in population]
    lengths = [len(ind) for ind in population]

    population_size = len(population)
    avg_fitness = sum(fitnesses) / population_size
    min_fitness = min(fitnesses)
    max_fitness = max(fitnesses)

    min_length = min(lengths)
    max_length = max(lengths)
    avg_length = sum(lengths) / population_size
    fittest_length = len(
        list(filter(lambda ind: ind.fitness.values[0] == min_fitness, population))[0])

    return (avg_fitness, min_fitness, max_fitness, min_length, max_length, avg_length, fittest_length)

# Genetic programming, based upon eaSimple
# https://github.com/DEAP/deap/blob/master/deap/algorithms.py
def gp_simple(population, cxpb, mutpb, ngen):
    hof = tools.HallOfFame(1)

    logbook = tools.Logbook()
    logbook.header = ['gen', 'avg', 'min', 'max', 'min_length',
                      'max_length', 'avg_length', 'fittest_length']

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hof.update(population)

    (avg, min, max, min_length, max_length,
     avg_length, fittest_length) = stats(population)
    logbook.record(gen=0, avg=avg, min=min, max=max, min_length=min_length,
                   max_length=max_length, avg_length=avg_length, fittest_length=fittest_length)

    print(logbook.stream)

    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        hof.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        (avg, min, max, min_length, max_length,
        avg_length, fittest_length) = stats(population)
        logbook.record(gen=gen, avg=avg, min=min, max=max, min_length=min_length,
                    max_length=max_length, avg_length=avg_length, fittest_length=fittest_length)

        print(logbook.stream)

    return logbook, hof


def main():
    pop = toolbox.population(n=1000)

    log, hof = gp_simple(pop, CROSSOVER_PROBABILITY,
                    MUTATION_PROBABILITY, ITERATIONS)

    print('Best individual throughout evolution with fitness ' + str(hof[0].fitness.values[0]) + ' was: ' + str(hof[0]))

    return log

def plot_a(log):
    fittest_per_iteration = log.select("min")

    _, ax = plt.subplots()
    ax.plot(list(range(ITERATIONS+1)), fittest_per_iteration)

    plt.xlabel('Iteration')
    plt.ylabel('Fitness of best individual')
    plt.show()


def plot_b(log):
    x = list(range(ITERATIONS+1))

    min_size_per_iteration = log.select("min_length")
    max_size_per_iteration = log.select("max_length")

    average_size_per_iteration = log.select("avg_length")
    fittest_size_per_iteration = log.select("fittest_length")
    
    _, ax = plt.subplots()
    ax.plot(x, fittest_size_per_iteration, color="green")
    ax.plot(x, average_size_per_iteration, color="blue")

    ax.fill_between(x, min_size_per_iteration, max_size_per_iteration, color='grey',alpha=0.5)

    plt.xlabel('Iteration')
    plt.ylabel('Number of nodes')
    plt.show()


if __name__ == "__main__":
    log = main()
    plot_a(log)
    # plot_b(log)
