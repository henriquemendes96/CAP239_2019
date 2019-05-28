import numpy as np


# Sum two signals, normalize between -1 and 1
def normalize(signal):
    return ((signal - min(signal))/(max(signal) - min(signal)) - 0.5) * 2


# Sum two signals, then standardize
def standardize(signal):
    return (signal - np.mean(signal))/np.std(signal)
