import math
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter1d

def pcorrect(c, p):
    v = math.floor(c / 2) + 1

    total_sum = 0

    for i in range(v, c + 1):
        total_sum += math.comb(c, i) * (p**i) * ((1 - p)**(c - i))

    return total_sum

# Exercise 2b.
print(pcorrect(19, 0.6))

# Exercise 2c.
competences = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
doctors = [1, 10, 19, 50]

for c in doctors:
    pcorrects = []

    for p in competences:
        pcorrects.append(pcorrect(c, p))
    
    plt.plot(competences, pcorrects, label=f"c = {c}")

plt.xlabel('Competence ($\it{p}$)')
plt.ylabel('Correct decision ($\it{pcorrect}$)')

plt.title('Correct decision probability graph')
 
plt.legend()
plt.show()
