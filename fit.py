import numpy as np
import scipy.stats as st
from powernoise import powernoise
import matplotlib.pyplot as plt


def fit_distributions(data, choice):
    distribution = [st.uniform, st.binom, st.beta, st.laplace, st.gamma,
                    st.expon, st.chi2, st.cauchy, st.norm]

    #for distribution in distributions:
    distribution = distribution[choice]
    params = distribution.fit(data)
    x = np.linspace(-5, 5, 100)
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    return distribution.pdf(x, loc=loc, scale=scale, *arg)


def main():
    S1 = powernoise(0, 2048)
    S1 = (S1 - np.mean(S1)) / np.std(S1)
    fitted_pdf = fit_distributions(S1, 8)
    x = np.linspace(-5, 5, 100)
    normal_pdf = st.norm.pdf(x)
    # Type help(plot) for a ton of information on pyplot
    plt.plot(x, fitted_pdf, "red", label="Fitted normal dist", linestyle="--", linewidth=2)
    plt.plot(x, normal_pdf, "blue", label="Normal dist", linestyle=":", linewidth=2)
    plt.hist(S1, normed=1, color="cyan", alpha=.5)  # alpha, from 0 (transparent) to 1 (opaque)
    plt.title("Normal distribution fitting")
    # insert a legend in the plot (using label)
    plt.legend()
    # we finally show our work
    plt.show()


if __name__ == '__main__':
    main()
