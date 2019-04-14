import numpy as np
'''
Sum two signals, normalize between -1 and 1 first and then normalize again with average equal to zero
'''


def normalize(signal1, signal2):
    signal_sum = signal1 + signal2
    return ((signal_sum - min(signal_sum))/(max(signal_sum) - min(signal_sum)) - 0.5) * 2;


def standardize(signal1, signal2):
    signal_sum = signal1 + signal2
    return (signal_sum - np.mean(signal_sum))/np.std(signal_sum)