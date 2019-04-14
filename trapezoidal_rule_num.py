# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np


def calculates_trapezoid_area(base1, base2, height):
    return ((base1 + base2) * height) / 2


def expression(n):
    return n**2 + 5


def plot_graph(limit_inf, limit_sup, num_trapezes, resolution):
    interval = np.arange(limit_inf, limit_sup, resolution)

    plt.figure(1)

    # Plots function
    plt.plot(interval, expression(interval), 'b')

    # Plots trapezes
    ticks = float((limit_sup - limit_inf)) / num_trapezes
    # Plots parallel lines
    lines_location_x = np.arange(limit_inf, limit_sup + 1e-10, ticks)

    for x in lines_location_x:
        plt.plot([x, x], [0, expression(x)], 'r')

    # Plots slanted lines
    for x in np.arange(limit_inf, limit_sup, ticks):
        plt.plot([x, x + ticks], [expression(x), expression(x + ticks)], 'r')

    plt.grid(True)
    plt.xticks(np.arange(min(interval), max(interval) + 1, 1))


def integral_trapezoidal(a, b, num_trapezes):
    i = a
    area = 0.0
    aux_count = 0
    while aux_count != num_trapezes:
        j = i + ((b - a) / num_trapezes)
        area += calculates_trapezoid_area(
            expression(i),
            expression(j),
            (b - a) / num_trapezes)
        i = j
        aux_count = aux_count + 1
    return area


def error_analysis(min_trapeze, max_trapeze, limit_inf, limit_sup, integral):
    relative_error_array = []
    for n in range(min_trapeze, max_trapeze + 1, 1):
        total_area = integral_trapezoidal(limit_inf, limit_sup, n)
        relative_error_array.append(abs((integral - total_area) / integral)*100)

    plt.figure(2)
    plt.plot(range(min_trapeze, max_trapeze + 1, 1), relative_error_array, 'b')
    plt.grid(True)
    plt.xlabel(u'Número de trapézios')
    plt.ylabel(u'Módulo do erro relativo [%]')
    plt.xticks(np.arange(min_trapeze, max_trapeze + 1, 7))
    plt.yticks(np.arange(0, max(relative_error_array), 5))


def main():
    # Inputs for the integration: inferior and superior limits and number of trapezes
    limit_inf = 0.0
    limit_sup = 12.0
    num_trapezes = 50
    resolution = 0.01  # Resolution of the interval, used to plot the graph

    # Inputs for the error analysis:
    min_trapeze = 1
    max_trapeze = 50

    # Trapezoidal Integration
    total_area = integral_trapezoidal(limit_inf, limit_sup, num_trapezes)

    integral = quad(expression, limit_inf, limit_sup)
    integral = integral[0]
    relative_error = (integral - total_area) / integral

    print('Area using trapezoidal rule: {:0.2f}'.format(total_area))
    print('Area using integral: {:0.2f}'.format(integral))
    print('Relative error: {:0.2f}%'.format(relative_error * 100))

    plot_graph(limit_inf, limit_sup, num_trapezes, resolution)

    error_analysis(min_trapeze, max_trapeze, limit_inf, limit_sup, integral)

    plt.show()


if __name__ == '__main__':
    main()
