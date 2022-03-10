import random
import math
import numpy as np
import statistics
import matplotlib as mpl
import matplotlib.pyplot as plt
def initialize(data, nr_particles, N):
    locations = np.random.choice(range(data.shape[0]), size=(nr_particles, N))
    return data[locations]

def fitness(centroids, data_labels, data, N):
    fitness = []
    for c, cent in enumerate(centroids):
        loc = np.where(data_labels == c)[0]
        distance = 0

        for l in loc:
            distance += np.linalg.norm(data[l] - cent) / loc.shape[0]
        fitness.append(distance/N)

    return sum(fitness)

def update_particle(x, v, x_lb, x_gb, r1, r2):
    omega = 0.72
    alpha1 = alpha2 = 1.49
    
    for i in range(0, x.shape[0]):
        v[i] = omega*v[i] + alpha1 * np.dot(r1, (x_lb[i] - x[i])) + alpha2 * np.dot(r2,  (x_gb - x[i]))

    x = x + v

    return x, v


def PSO_clustering(data, nr_particles, N, max_iter):

    x = initialize(data, nr_particles, N)
    v = np.zeros_like(x)

    r1 = np.random.random(size=N)
    r2 = np.random.random(size=N)

    local_bests = x
    fit_lb = np.ones((x.shape[0])) * np.inf
    global_best = None
    fit_gb = np.inf
   
    # Iterations
    for iter in range(0, max_iter):
        fitnesses = np.zeros((x.shape[0]))
        # Particles
        for i in range(0, x.shape[0]):

            # Data labels
            data_labels = np.zeros(data.shape[0])

            # Data point
            for j in range(0, data.shape[0]):

                # Euclidian distances
                distances = np.zeros(x.shape[1])

                # Centroid
                for c, centroid in enumerate(x[i]):
                    distances[c] = np.linalg.norm(centroid - data[j])

                data_labels[j] = np.argmin(distances)

            fit = fitness(x[i], data_labels, data, N)
            fitnesses[i] = fit
            if fit < fit_lb[i]:
                local_bests[i] = x[i]
                fit_lb[i] = fit
        
        if min(fitnesses) < fit_gb:
            global_best = x[np.argmin(fitnesses)]
            fit_gb = min(fitnesses)

        x, v = update_particle(x, v, local_bests, global_best, r1 , r2)
    
    return x, data_labels

def cluster_compare(data, classes, title):
    trial = 30
    N = np.unique(classes).shape[0]
    nr_particles = 10
    PSO_f = np.zeros((trial,nr_particles))
    km_f = np.zeros((trial))
    max_iter = 100
    for i in range(0,trial):
        particles, pso_classes = PSO_clustering(data, nr_particles, N, max_iter)

        PSO_f[i] = [fitness(p, classes, data, N) for p in particles]

    fig, ax = plt.subplots()
   
    ax.scatter(data[:,1], data[:,0],c=pso_classes)
    ax.set_title("PSO Clusters")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plt.show()


data = np.random.uniform(-1,1,size=(400,2))
classes = np.array([1 if d[0] >= 0.7 or (d[0] <= 0.3 and d[1] >= -0.2-d[0]) else 0 for d in data])
cluster_compare(data, classes, "Artificial Dataset 1")
cluster_compare(data, classes, "Iris Dataset")