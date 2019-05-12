import numpy as np
from random import uniform
import scipy.stats as st
import matplotlib.pyplot as plt

def generateGalaxies():
    galaxies = np.random.choice(['Irregular', 'Spiral', 'Elliptical'], 2000, p=[0.1667, 0.5166, 0.3167])
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
    names, values = generateGalaxies()

    np.savetxt('galaxies.txt', zip(values), fmt='%5.10f')

    mean, std = st.norm.fit(values)
    print(mean,std)
    maxValue = max(values)
    print(maxValue)

    print(st.kstest(values, st.norm.cdf, [mean, std]))

    plt.hist(values, bins=20, density=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = st.norm.pdf(x, mean, std)
    plt.plot(x, y, 'r', lw=3)
    plt.grid(True)
    plt.show()



# Avoids the entire program running when it is import as library by another script
if __name__ == '__main__':
    main()
