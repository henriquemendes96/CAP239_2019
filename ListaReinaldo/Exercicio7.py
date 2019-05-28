import matplotlib.pyplot as plt
from mfdfa import hurst, basic_dfa
from logistic import logistic
from pmodel import pmodel
import preprocess as pre
from powernoise import powernoise
import numpy as np

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

n_samples = 1024

np.savetxt('S8.txt', data)

'''
ans = hurst(S3, skip_agg=True)
print(ans)

qorders = list(range(0, 50))
generalized_hurst_expornents = basic_dfa(S3, Q=qorders, skip_agg=True)
plt.plot(qorders, generalized_hurst_expornents)
plt.show()
'''