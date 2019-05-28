import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from pandas_datareader import data as wb


def monteCarlo(select):

    if select == 'online':
        ticker = 'AAPL'  # Company being analysed (Apple in this case)
        data = pd.DataFrame()  # Creates a dataframe
        data[ticker] = wb.DataReader(ticker, data_source='yahoo', start='2009-1-1')['Adj Close']
    else:
        with open('objs.pkl') as f:
            data = pickle.load(f)

#    data.plot(figsize=(10, 6))
    log_returns = np.log(1 + data.pct_change())
    log_returns.tail()
#    log_returns.plot(figsize=(10, 6))
    u = log_returns.mean()
    var = log_returns.var()
    stdev = log_returns.std()
    drift = u - (0.5 * var)
    t_intervals = 252
    iterations = 10000
    Z = norm.ppf(np.random.rand(t_intervals, iterations))
    daily_returns = np.exp(drift.values + stdev.values * Z)
    S0 = data.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0

    for t in range(1, t_intervals):
        price_list[t] = price_list[t-1] * daily_returns[t]

    price_final = price_list[-1, :]

    save(data)

    return price_list, price_final


def plotting(price_list, price_final):
    plt.figure(figsize=(10, 5))
    plt.plot(price_list)
    plt.grid(True)
    plt.title('All Stocks')
    plt.xlabel('Time from now [days]')
    plt.ylabel('Stock Price [USD]')
    plt.show()

    mean, std = norm.fit(price_final)
    plt.hist(price_final, bins=100, density=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y)
    plt.axvline(np.percentile(price_final, 5), color='r', linestyle='dashed', linewidth=2)
    plt.axvline(np.percentile(price_final, 95), color='r', linestyle='dashed', linewidth=2)
    plt.grid(True)
    plt.title('Histogram vs Fitted Gaussian [normalized]')
    plt.xlabel('Bins')
    plt.ylabel('Probability density')
    plt.show()

    n, bin_edges, patches = plt.hist(price_final, bins=100, density=False)
    y = y * ((bin_edges[-1] - bin_edges[0]) / 100 * len(price_final))
    plt.plot(x, y)
    plt.axvline(np.percentile(price_final,5), color='r', linestyle='dashed', linewidth=2)
    plt.axvline(np.percentile(price_final,95), color='r', linestyle='dashed', linewidth=2)
    plt.grid(True)
    plt.title('Histogram vs Fitted Gaussian')
    plt.xlabel('Bins')
    plt.ylabel('Stock Price [USD]')
    plt.show()


def save(data):
    with open('objs.pkl', 'wb') as f:
        pickle.dump(data, f)


def main():
    selection = 'online'
    price_list, price_final = monteCarlo(selection)

    # use numpy mean function to calculate the mean of the result
    print('Average stock price = %.2f' % np.around(np.mean(price_list),2))
    print('5% ' + 'quantile = %.2f' % np.around(np.percentile(price_list,5),2))
    print('95% ' + 'quantile = %.2f' % np.around(np.percentile(price_list,95),2))

    # create histogram of ending stock values for our multiple simulations
    mean, std = norm.fit(price_final)
    hist, bin_edges = np.histogram(price_final,bins=100, density=True)
    print('Max probability density for fitted Gaussian is: %.4f' % norm.pdf(mean, mean, std))
    print('Max probability density for normalized histogram is: %.4f' % max(hist))

    plotting(price_list, price_final)


if __name__ == '__main__':
    main()


