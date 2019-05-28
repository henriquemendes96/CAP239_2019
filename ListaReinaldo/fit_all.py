import numpy as np
import scipy.stats as st
from powernoise import powernoise
import matplotlib.pyplot as plt
import preprocess as pre

# Exercicio 2.1
def fit_distribution(data, distribution):
    params = distribution.fit(data)
    x = np.linspace(-5, 5, 2048)
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    return distribution.pdf(x, loc=loc, scale=scale, *arg)


def main():
    S1 = powernoise(0, 2048)
    S1 = pre.standardize(S1)
    fitted_pdf = np.zeros((9, 2048))
    distribution = [st.uniform, st.norm, st.beta, st.laplace, st.gamma,
                    st.expon, st.chi2, st.cauchy, st.norm]
    for n in range(0, 9, 1):
        fitted_pdf[n, :] = fit_distribution(S1, distribution[n])

    x = np.linspace(-5, 5, 2048)
    normal_pdf = st.norm.pdf(x)

    plt.plot(x, fitted_pdf[8, :], "red", label="Fitted normal dist", linestyle="--", linewidth=2)
    plt.plot(x, normal_pdf, "blue", label="Normal dist", linestyle=":", linewidth=2)
    plt.hist(S1, density=1, color="cyan", label="Data", alpha=.5)
    plt.title("Normal distribution fitting")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
