import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

# Exercicio 2.2
n = 100
p = 1.0/6
k = np.arange(0, n)

data = st.binom.pmf(k, n, p)
print("Mean: %f" % np.mean(data))
print("Standard deviation: %f" % np.std(data))
plt.bar(k, data)
plt.ylabel('Probability')
plt.xlabel('Number of dice')
plt.xlim(0, 35)
plt.show()
