from scipy.stats import kurtosis, skew
from powernoise import powernoise
import matplotlib.pyplot as plt
import numpy as np

galaxies = np.loadtxt('galaxies.txt')

# As a test, lets calculate the Cullen-Frey location of a
# white-noise, which has a gaussian normal distribution
S1 = powernoise(0, 1024) # White Noise
x = np.random.normal(10, 2, 10000)
print('Kurtosis of normal distribution (should be approximately 3): {}'.format(kurtosis(S1,fisher=False)))
print('Skewness of normal distribution (should be approximately 0): {}'.format(skew(S1)))
plt.plot(skew(S1)**2, kurtosis(S1,fisher=False),'m*')

galaxies_kurtosis = []
galaxies_skewness = []

for column in galaxies.T:
    galaxies_kurtosis.append(kurtosis(column, fisher=False))
    galaxies_skewness.append(skew(column))

galaxies_skewness = np.asarray(galaxies_skewness)
galaxies_kurtosis = np.asarray(galaxies_kurtosis)

for i in range(0, 10, 1):
    x = galaxies_skewness[i]**2
    y = galaxies_kurtosis[i]
    plt.plot(x, y, 'b*')

plt.grid('True')
plt.xlabel('Skewness Squared')
plt.ylabel('Kurtosis')
plt.show()