# Portfilo Matrices     #don't forget to add stock prices and how many to purchase given weights
import numpy as np
import fix_yahoo_finance as yf
import pandas_datareader as pdr
stocks = ['CBA.AX', 'WOW.AX', 'BHP.AX', 'A2M.AX']
ones = []
for i in stocks:
    ones.append(1)
print(ones)

stock_data = pdr.get_data_yahoo(stocks)['Adj Close']
avg_ret = np.average(np.log(stock_data / stock_data.shift(1))*252)
returns = []
for i in stocks:
    returns.append(avg_ret)
print(returns)
