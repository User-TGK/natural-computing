import math
import random
import statistics
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def iris() -> list[list[float]]:
    with open('iris.data', 'r') as f:
        return [
            [float(x) for x in line.split(',')[:4]]
            for line in f
        ]


def artificial1() -> tuple[list[list[float]], list[int]]:
    with open('artificial1.data', 'r') as f:
        z = []
        ac = []
        for line in f:
            z1, z2, c = line.split(',')
            z.append([float(z1), float(z2)])
            ac.append(int(c))

        return z, ac


def dist(x: list[float], y: list[float]) -> float:
    return math.sqrt(sum((i - j)**2 for (i, j) in zip(x, y)))


def kmeans(Nd: int, No: int, Nc: int, z: list[list[float]], tmax=100) -> tuple[list[int], list[list[float]]]:
    """
    Nd: input dimension
    No: number of vectors
    Nc: number of clusters
    z:  dataset
    """

    m = [random.choice(z) for _ in range(Nc)] # centroids (seeded from the data set)

    cluster = [None for _ in range(No)] # mapping of data vector p to cluster j

    for _ in range(tmax):
        for p, zp in enumerate(z):
            jmin = None
            dmin = math.inf

            for j, mj in enumerate(m):
                d = dist(zp, mj)
                if d < dmin:
                    jmin = j
                    dmin = d

            cluster[p] = jmin

        for j in range(Nc):
            Cj = [zp for p, zp in enumerate(z) if cluster[p] == j] # data vectors in cluster j
            nj = len(Cj) # number of vectors in cluster j

            if nj != 0:
                mj_next = [0 for _ in range(Nd)] # updated centroid
                for zp in Cj:
                    for k, x in enumerate(zp):
                        mj_next[k] += x

                for k in range(Nd):
                    mj_next[k] /= nj

                m[j] = mj_next

    return cluster, m


def quantization_error(z: list[list[float]], m: list[list[float]], cluster: list[int]) -> float:
    err = 0

    for j, mj in enumerate(m):
        Cj = [zp for p, zp in enumerate(z) if cluster[p] == j]
        nj = len(Cj)

        if nj == 0:
            continue

        avg_dist = 0
        for zp in Cj:
            avg_dist += dist(zp, mj)

        err += avg_dist/nj

    return err/len(m)


def main():
    err_iris = []
    err_artificial1 = []

    Nd_iris = 4
    No_iris = 150
    Nc_iris = 3
    z_iris = iris()

    Nd_artificial1 = 2
    No_artificial1 = 400
    Nc_artificial1 = 2
    z_artificial1, ac_artificial1 = artificial1()

    for _ in range(30):
        cluster, m = kmeans(Nd_iris, No_iris, Nc_iris, z_iris)
        err_iris.append(quantization_error(z_iris, m, cluster))

        cluster, m = kmeans(Nd_artificial1, No_artificial1, Nc_artificial1, z_artificial1)
        err_artificial1.append(quantization_error(z_artificial1, m, cluster))

    print('iris\t\t', f'{statistics.mean(err_iris):.3f} {statistics.stdev(err_iris):.3f}')
    print('artificial1\t', f'{statistics.mean(err_artificial1):.3f} {statistics.stdev(err_artificial1):.3f}')

    # TODO: visualize iris

    cluster, m = kmeans(Nd_artificial1, No_artificial1, Nc_artificial1, z_artificial1)

    # Color mapping for clusters (0 = red, 1 = blue)
    cmap = mpl.colors.ListedColormap([[1., 0., 0.], [0., 0., 1.]])

    fig, axes = plt.subplots()
    plt.xlabel('z1')
    plt.ylabel('z2')

    # Plot found clusters

    x, y = np.array(z_artificial1).T
    axes.scatter(x, y, c=cluster, cmap=cmap)

    # Plot found centroids

    mx, my = np.array(m).T
    axes.plot(mx, my, 'ko')

    # Plot actual clusters

    fig, axes = plt.subplots()
    plt.xlabel('z1')
    plt.ylabel('z2')

    axes.scatter(x, y, c=ac_artificial1, cmap=cmap)

    plt.show()


if __name__ == '__main__':
    main()
