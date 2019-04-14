import numpy as np
import math


def powernoise(beta, N):
    opt_randpow = False
    opt_normal = False

    N2 = N / 2 - 1
    f = np.arange(2, (N2 + 1) + 1, 1)
    A2 = 1.0 / (f ** (beta / 2.0))

    if not opt_randpow:
        p2 = (np.random.uniform(0, 1, N2) - 0.5) * 2 * math.pi
        d2 = A2 * np.exp(1j * p2)
    else:
        p2 = np.random.rand(N2) + 1j * np.random.rand(N2)
        d2 = A2 * p2

    d = np.concatenate(([1], d2, [1.0/((N2 + 2.0) ** beta)], np.flipud(np.conjugate(d2))))
    x = np.real(np.fft.ifft(d))

    if opt_normal:
        x = ((x - min(x)) / (max(x) - min(x)) - 0.5) * 2

    return x


def main():
    n_samples = 2**12
    beta = [0, 1, 2]
    S1 = powernoise(beta[0], n_samples)
    S2 = powernoise(beta[1], n_samples)
    S3 = powernoise(beta[2], n_samples)


if __name__ == '__main__':
    main()
