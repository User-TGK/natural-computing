import random
import math
import numpy as np

def iris() -> list[list[float]]:
    with open('iris.data', 'r') as f:
        return [
            [float(x) for x in line.split(',')[:4]]
            for line in f
        ]

def artificial1() -> list[list[float]]:
    with open('artificial1.data', 'r') as f:
        return [
            [float(x) for x in line.split(',')[:2]]
            for line in f
        ]

def dist(x: list[float], y: list[float]) -> float:
    return math.sqrt(sum((i - j)**2 for (i, j) in zip(x, y)))

class Partical:
    def __init__(self, nc, dataset):
        self.nc = nc
        self.centroids = []
        self.velocity = []
        self.local_best = None

        for c in [random.choice(dataset) for _ in range(nc)]:
            self.centroids.append(Centroid(c))
            self.velocity.append([0.0 for _ in range(len(c))])

    def __repr__(self):
        return str(self.centroids)

    def update(self, omega, alpha, r, global_best):        
        for i, c in enumerate(self.centroids):
            vel = np.array(self.velocity[i])
            pos = np.array(c.value())
            
            glob = np.array(global_best[i].value())
            loc = np.array(self.local_best[i].value())

            self.velocity[i] = (omega * vel + alpha*r*(loc - pos) + alpha*r*(glob - pos)).tolist()
            self.centroids[i] = Centroid((pos + self.velocity[i]).tolist())

    def clear_assigned_points(self):
        for c in self.centroids:
            c.points = []

    def update_local_best(self):
        fitness = self.compute_fitness(self.centroids)

        if self.local_best == None:
            self.local_best = self.centroids

        elif fitness < self.compute_fitness(self.local_best):
            self.local_best = self.centroids

    def compute_fitness(self, centroids):
        quantization_error_sum = 0

        for c in centroids:
            total_distance = 0

            for z in c.points:
                total_distance += dist(c.value(), z)

            if len(c.points) != 0:
                quantization_error_sum += (total_distance / len(c.points))

        quantization_error = quantization_error_sum / len(centroids)
        return quantization_error

class Centroid:
    def __init__(self, c):
        self.centroid = c
        self.points = []

    def __repr__(self):
        return f"centroid: {self.centroid}\n assigned points: {self.points}"

    def value(self):
        return self.centroid

    def append_point(self, point):
        self.points.append(point)

def compute_global_best(old_global_best, particals):
    global_best = old_global_best
    
    for p in particals:
        if global_best == None:
            global_best = p.local_best
        elif p.compute_fitness(p.local_best) < p.compute_fitness(global_best):
            global_best = p.local_best

    return global_best

def pso_clustering(nc, z, t_max, omega, alpha, r):
    nr_of_particals = 10
    particals = []
    global_best = None

    # Initialize each particle to contain N randomly selected centroids
    for _ in range(nr_of_particals):
        particals.append(Partical(nc, z))

    for t in range(t_max):
        for partical in particals:
            partical.clear_assigned_points()
            for p in z:
                imin = None
                dmin = math.inf

                for i, c in enumerate(partical.centroids):
                    d = dist(p, c.value())
                    if d < dmin:
                        imin = i
                        dmin = d

                # Assign p to the centroid whose eucledian distance is smallest
                partical.centroids[imin].append_point(p)

            partical.update_local_best()
        
        global_best = compute_global_best(global_best, particals)

        if t == t_max-1:
            return global_best

        for partical in particals:
            partical.update(omega, alpha, r, global_best)
    
    return global_best

def main():
    solution = pso_clustering(nc=3, z=iris(), t_max=100, omega=0.62, alpha=1.49, r=1.0)

    # solution = pso_clustering(nc=2, z=artificial1(), t_max=100, omega=0.55, alpha=1.49, r=1.0)

    print(solution)

if __name__ == '__main__':
    main()
