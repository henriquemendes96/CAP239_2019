from scipy.stats import kurtosis, skew
from powernoise import powernoise
import numpy as np

S1 = powernoise(0, 1024) # White Noise
x = np.random.normal(10, 2, 10000)

print('Kurtosis of normal distribution (should be 3): {}'.format(kurtosis(S1,fisher=False)))
print('Skewness of normal distribution (should be 0): {}'.format(skew(S1)))
