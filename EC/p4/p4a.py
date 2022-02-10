import random
import matplotlib.pyplot as plt


def mutate(bit: int, p: float) -> int:
    if random.random() <= p:
        return 1 - bit

    return bit


def main():
    l = 100
    p = 1/100
    iterations = 1500

    ind = [random.getrandbits(1) for _ in range(l)]

    max_fitness = 0
    max_fitnesses = []

    for _ in range(iterations):
        offspring = [mutate(bit, p) for bit in ind]

        ind_fitness = sum(ind)
        offspring_fitness = sum(offspring)

        if offspring_fitness > ind_fitness:
            ind = offspring

        max_fitness = max(max_fitness, ind_fitness, offspring_fitness)
        max_fitnesses.append(max_fitness)

    fig, ax = plt.subplots()
    ax.plot(list(range(1, iterations+1)), max_fitnesses)
    plt.xlabel('iterations')
    plt.ylabel('fitness')
    plt.show()


if __name__ == '__main__':
    main()
