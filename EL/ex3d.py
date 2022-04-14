import math
import matplotlib.pyplot as plt

m = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
error_m = []
alpha_m = []

for p in m:
    error = 1 - p
    error_m.append(error)
    alpha_m.append(math.log((1-error)/error))

plt.plot(error_m[::-1], alpha_m[::-1])
plt.title('Base learner')
plt.xlabel('Error probability p')
plt.ylabel('Weight w')
plt.savefig('Figure_2.png')
plt.show()
