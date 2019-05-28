import numpy as np
import math


def next_step_1d(y, p):
    length = len(y)
    y2 = np.zeros(length * 2)
    sign = np.random.uniform(0, 1, length) - 0.5
    sign = sign / abs(sign)
    y2[::2] = y + sign * (1 - 2 * p) * y
    y2[1::2] = y - sign * (1 - 2 * p) * y

    return y2


def fractal_spectrum_1d(noValues, slope):
    # If you want to make a large number of time series, please rewrite this part to get rid of the for loop
    ori_vector_size = noValues
    ori_half_size = int(ori_vector_size / 2)
    # The magnitudes of the Fourier coefficients
    a = np.zeros(ori_vector_size)

    for t2 in range(1, (ori_half_size + 1) + 1, 1):
        index = t2 - 1
        t4 = 2 + ori_vector_size - t2
        if t4 > ori_vector_size:
            t4 = t2
        # The following condition was added because Matlab allows 0 to the negative power
        if index == 0:
            coeff = 1
        else:
            coeff = index ** slope
        a[t2 - 1] = coeff
        a[t4 - 1] = coeff

    a[0] = 0  # The DC-component of the Fourier spectrum should be zero
    return a


def pmodel(**kwargs):

    noValues = kwargs.get('noValues')
    p = kwargs.get('p')
    slope = kwargs.get('slope')

    if len(kwargs) < 1 or kwargs.get('noValues') == 'None':
        noValues = 256
    if len(kwargs) < 2 or kwargs.get('p') == 'None':
        p = 0.375
    if len(kwargs) < 3:
        slope = 'empty'

    # Calculate length of time series
    noOrders = int(math.ceil(math.log(noValues, 2)))

    # y is the time series generated with the p-model.
    y = [1]
    temp = 0
    for n in range(1, noOrders + 1, 1):
        temp = temp + 1
        y = next_step_1d(y, p)

    # If a slope if specified also a fractionally integrated time series(x) is calculated from y.
    if not slope == 'empty':
        fourierCoeff = fractal_spectrum_1d(noValues, slope / 2)
        # Calculate the magnitudes of the coefficients of the Fourier spectrum.
        # The Fourier slope is half of the slope of the power spectrum.
        meanVal = np.mean(y)
        stdy = np.std(y)
        # Calculate the Fourier coefficients of the original p-model time series
        x = np.fft.ifft(y - meanVal)
        # Calculate the phases, as these are kept intact, should not be changed by the Fourier filter
        phase = np.angle(x)
        # Calculate the complex Fourier coefficients with the specified spectral slope, and the phases of the p-model
        x = fourierCoeff * np.exp(1j * phase)
        # Generate the fractionally integrated time series.
        x = np.real(np.fft.fft(x))
        x = x * stdy / np.std(x)
        x = x + meanVal
    else:
        x = y

    y = y[0:noValues + 1]
    x = x[0:noValues + 1]

    return x
