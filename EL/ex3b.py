from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from operator import mul, concat


def concatLists(xs):
    return reduce(concat, xs, [])

def product(xs):
    return reduce(mul, xs, 1)

def intersect(xs, ys):
    return [item for item in xs if item not in ys]

class Classifier:
    def __init__(self,p,w):
        self.p = p
        self.w = w

def load_classifiers(n):
    result = []
    for _ in range(n):
        result.append(Classifier(0.6,1))
    return result

def calculate(w):
    classifiers = load_classifiers(10)
    classifiers.append(Classifier(0.8,w))
    majority_vote = (sum(map(lambda x: x.w, classifiers)) / 2)
    all_combinations = concatLists([list(combinations(classifiers, i)) for i in range(11+1)])
    majority_combinations = (filter(lambda combination: sum(map(lambda x:x.w, combination)) > majority_vote, all_combinations))

    result = 0
    for maj_combination in majority_combinations:
        result += product((map(lambda x: x.p, maj_combination))) * product((map(lambda classifier: 1 - classifier.p, intersect(classifiers, maj_combination))))
    return result

x = np.linspace(0, 10, 100)
y = list(map(calculate, x))
plt.plot(x, y)
plt.xlabel("Weight w for the strong classifier")
plt.ylabel("Probability p of the correct decision")
plt.title("Weighted classifier comparison")
plt.show()

