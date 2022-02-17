import math
import random

import matplotlib.pyplot as plt


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


def kmeans(Nd: int, No: int, Nc: int, z: list[list[float]], tmax=1000) -> list[int]:
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

    return cluster


def main():
    print(kmeans(Nd=4, No=150, Nc=3, z=iris()))

    print(kmeans(Nd=2, No=400, Nc=2, z=artificial1()))


if __name__ == '__main__':
    main()
