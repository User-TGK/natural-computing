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
    runs = 10

    optimum_found = 0
    overall_max_fitness = 0

    _fig, ax = plt.subplots()

    for _ in range(runs):
        ind = [random.getrandbits(1) for _ in range(l)]

        max_fitness = 0
        max_fitnesses = []

        for _ in range(iterations):
            offspring = [mutate(bit, p) for bit in ind]
            ind = offspring

            max_fitness = max(max_fitness, sum(ind))
            max_fitnesses.append(max_fitness)

        ax.plot(list(range(1, iterations+1)), max_fitnesses)

        if max_fitnesses[-1] == l:
            optimum_found += 1

        overall_max_fitness = max(overall_max_fitness, max_fitnesses[-1])

    print(optimum_found)
    print(overall_max_fitness)

    plt.xlabel('iterations')
    plt.ylabel('fitness')
    plt.show()


if __name__ == '__main__':
    main()
