# Portfilo Matrices     #don't forget to add stock prices and how many to purchase given weights
import numpy as np
import fix_yahoo_finance as yf
import pandas_datareader as pdr

stocks = ['CBA.AX', 'WOW.AX', 'BHP.AX']
# ONE VECTOR
ones = []
for i in stocks:
    ones.append(1)
one = np.array(ones)
print('Ones')
print(one)

# RETURN VECTOR
stock_data = pdr.get_data_yahoo(stocks)['Adj Close']
ret = np.log(stock_data / stock_data.shift(1))
retvect = np.array((np.mean(ret)*252))
print('Return Vector')
print(retvect)

# WEIGHT VECTOR
weights = np.random.rand(len(stocks))
weights /= np.sum(weights)
print('Weights Vector')
print(weights)

# COVARIANCE MATRIX
retcov = np.array(ret.cov()*252)
invretcov = np.matrix(retcov).I
print('Variance Co-Variance Matrix')
print(retcov)
print(invretcov)

# A CALCUATION
A = np.dot(one, np.dot(invretcov, np.transpose(one)))
print('A')
print(A)

# B CALCULATION
B = np.dot(one, np.dot(invretcov, retvect))
print('B')
print(B)
