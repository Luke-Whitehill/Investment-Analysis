# Portfilo Matrices     #don't forget to add stock prices and how many to purchase given weights
import numpy as np
import fix_yahoo_finance as yf
import pandas_datareader as pdr

stocks = ['CBA.AX', 'WOW.AX', 'BHP.AX', 'A2M.AX', 'MQG.AX',
          'BOQ.AX', 'NAB.AX', 'CTX.AX', 'FMG.AX', 'A40.AX']
# ONE VECTOR
ones = []
for i in stocks:
    ones.append(1)
print(ones)

# RETURN VECTOR
stock_data = pdr.get_data_yahoo(stocks)['Adj Close']
retvect = np.mean(np.log(stock_data / stock_data.shift(1))*252).tolist()
print(retvect)

# WEIGHT VECTOR
weights = []
for i in stocks:
    weights.np.random()


# COVARIANCE MATRIX
