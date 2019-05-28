from pmodel import pmodel
from powernoise import powernoise
from logistic import logistic
import preprocess as pre
import matplotlib.pyplot as plt


def main():
    n_samples = 4096
    beta = [0, 1, 2]
    p = [0.52, 0.62, 0.72]
    slope = [-1.66, -0.45, -0.75]
    # O exercicio pede 3.85, mas 4 é caos puro, a figura fica perfeita
    rho = 3.85
    a0 = 0.001
    # Exercicio 1.1
    S1 = powernoise(beta[0], n_samples)
    S2 = powernoise(beta[1], n_samples)
    S3 = powernoise(beta[2], n_samples)
    # Exercicio 1.2
    S4 = logistic(rho, a0, n_samples)
    # Exercicio 1.3
    S5 = pre.standardize(S1 + S4)
    S6 = pre.standardize(S2 + S4)
    S7 = pre.standardize(S3 + S4)
    # Exercicio 1.4
    S8 = pmodel(noValues=n_samples, p=p[0], slope=slope[0])
    S9 = pmodel(noValues=n_samples, p=p[1], slope=slope[1])
    S10 = pmodel(noValues=n_samples, p=p[2], slope=slope[2])

    plt.figure(1)
    plt.plot(S4[0:n_samples-1], S4[1:n_samples], 'b*')
    plt.xlabel('A[n]')
    plt.ylabel('A[n+1]')
    plt.title('Logistic Map')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
