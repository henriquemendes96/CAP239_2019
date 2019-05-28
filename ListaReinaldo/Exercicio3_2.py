import numpy as np
from random import uniform
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew

def generateGalaxies():
    galaxies = np.random.choice(['Irregular', 'Spiral', 'Elliptical'], 200, p=[0.1667, 0.5166, 0.3167])
    galaxyValue = []

    for galaxy in galaxies:
        if galaxy == 'Irregular':
            galaxyValue.append(round(uniform(1.97, 1.99), 10))
        elif galaxy == 'Spiral':
            galaxyValue.append(round(uniform(1.96, 1.98), 10))
        elif galaxy == 'Elliptical':
            galaxyValue.append(round(uniform(1.92, 1.96), 10))

    return galaxies, galaxyValue


def main():
    names = np.chararray((200,10))
    values = np.zeros((200, 10))

    for i in range(0,10,1):
        names[:,i], values[:,i] = generateGalaxies()

    # np.savetxt('galaxies.txt', zip(values), fmt='%5.10f')

    # Fazendo o ajuste em uma das amostras (primeira)
    sample = 0
    mean, std = st.norm.fit(values[:,sample])
    print(mean, std)
    maxValue = max(values[:,sample])
    print(maxValue)

    print(st.kstest(values[:,sample], st.norm.cdf, [mean, std]))
    # p-value e pequeno, portanto o fit e valido

    n, bin_value, patch = plt.hist(values[:,sample], bins=50, density=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = st.norm.pdf(x, mean, std)
    plt.plot(x, y, 'r', lw=3)
    plt.grid(True)
    plt.show()

    maxHist = max(n)
    maxNorm = st.norm.pdf(mean, mean, std)

    mle = abs(maxHist - maxNorm)
    print('Max likelihood is ',mle)

    print(kurtosis(values[:,sample],fisher=False))
    print(skew(values[:,sample]))

if __name__ == '__main__':
    main()
