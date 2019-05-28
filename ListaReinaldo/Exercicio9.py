import numpy as np
from powernoise import powernoise
from logistic import logistic
from pmodel import pmodel
import preprocess as pre
import waipy


def main():
    n_samples = 1024
    # Ruido vermelho
    S3 = powernoise(2, n_samples)

    # Caos, usado para gerar o sinal S7
    rho = 3.85
    a0 = 0.001
    S4 = logistic(rho, a0, n_samples)

    # Soma os sinais e normalizae modo que <A>=0 e std=1
    S7 = pre.standardize(S3 + S4)

    # Sinal gerado pelo pmodel
    S8 = pmodel(noValues=n_samples, p=0.52, slope=-1.66)

    data = S8

    z = np.linspace(0, 1024, 1024)

    data_norm = waipy.normalize(data)
    result = waipy.cwt(data_norm, 1, 1, 0.125, 2, 4 / 0.125, 0.72, 6, mother='Morlet', name='S8')
    waipy.wavelet_plot('S8', z, data_norm, 0.03125, result)


if __name__ == "__main__":
    main()