import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plt.style.use('seaborn-whitegrid')

SETTING_1 = (0.5, 1.5, 0.5)
SETTING_2 = (0.7, 1.5, 1.0)

def f(x):
    return x**2

def update(velocity, position, omega, alpha_1, r_1, alpha_2, r_2, personal_best, social_best):
    return (omega * velocity + alpha_1 * r_1 * (personal_best - position) +  alpha_2 * r_2 * (social_best - position))

def trajectory(setting):
    (omega, alpha, r) = setting
    velocity = 10
    position = 20

    trajectory = [(position, f(position))]

    personal_best = position
    social_best = position

    last_position = -1

    while True:
        velocity = update(velocity, position, omega, alpha, r, alpha, r, personal_best, social_best)
        position = position + velocity

        res = f(position)

        if res < f(personal_best):
            personal_best = position
        if res < f(social_best):
            social_best = position

        trajectory.append((position, res))

        if abs(position - last_position) < 0.001:
            break

        last_position = position

    return trajectory

def plot_fitness(trajectory, ax, color, with_x_label=False):
    positions, fitnesses = zip(*trajectory)
    iterations = list(range(len(positions)))

    ax.plot(iterations, fitnesses, 'o', color=color)

    plt.xlabel('Iteration')
    plt.ylabel('Fitness')

    if with_x_label:

        for i, p in enumerate(positions):
            plt.text(iterations[i], fitnesses[i], f"x: {p}")

def plot_trajectory(trajectory, ax, color):
    positions, _fitnesses = zip(*trajectory)
    iterations = list(range(len(positions)))

    ax.plot(iterations, positions, 'o', color=color)

    plt.xlabel('Iteration')
    plt.ylabel('Position')

def main():
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    setting_1_trajectory = trajectory(SETTING_1)
    setting_2_trajectory = trajectory(SETTING_2)

    # Uncomment this block to plot the fitnesses
    # plot_fitness(setting_1_trajectory, ax, "blue")    
    # plot_fitness(setting_2_trajectory, ax, "green")

    # Uncomment this block to plot the trajectories
    # plot_trajectory(setting_1_trajectory, ax, "blue")    
    plot_trajectory(setting_2_trajectory, ax, "green")

    plt.show()

if __name__ == "__main__":
    main()
