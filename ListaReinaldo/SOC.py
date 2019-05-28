import numpy as np
import matplotlib.pyplot as plt
from mfdfa import hurst, basic_dfa
from powernoise import powernoise
from logistic import logistic
from pmodel import pmodel
import preprocess as pre

def SOC(data):
    # Taxa local de flutuação
    data_mean = np.mean(data)
    data_std = np.std(data)
    gamma = (data - data_mean)/data_std
    hist, bin_edges = np.histogram(data)
    P_gamma = hist / 1024
    return gamma, P_gamma, hist

def main():
    n_samples = 1024
    # Ruido vermelho
    S3 = powernoise(2, n_samples)

    # Caos, usado para gerar o sinal S7
    rho = 3.85
    a0 = 0.001
    S4 = logistic(rho, a0, n_samples)

    # Soma os sinais e normaliza de modo que <A>=0 e std=1
    S7 = pre.standardize(S3 + S4)

    # Sinal gerado pelo pmodel
    S8 = pmodel(noValues=n_samples, p=0.52, slope=-1.66)

    data = S3

    gamma, P_gamma, ni = SOC(data)
    plt.plot(np.log10(P_gamma),np.log10(ni))
    plt.show()

if __name__ == "__main__":
    main()