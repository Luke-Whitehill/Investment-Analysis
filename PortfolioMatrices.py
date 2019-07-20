# Portfilo Matrices     #don't forget to add stock prices and how many to purchase given weights
import numpy as np
import fix_yahoo_finance as yf
import pandas_datareader as pdr

print('Enter your desired portfolio return...')
target_return = np.matrix(input())
stocks = ['CBA.AX', 'WOW.AX', 'BHP.AX', 'A40.AX', 'AGL.AX', 'CTX.AX',
          'MQG.AX', 'MFG.AX', 'NEC.AX', 'QAN.AX', 'RIO.AX', 'S32.AX', 'DMP.AX']
# ONE VECTOR
ones = []
for i in stocks:
    ones.append(1)
one = np.matrix(ones)
invone = np.matrix.transpose(one)

# RETURN VECTOR
stock_data = pdr.get_data_yahoo(stocks)['Adj Close']
ret = np.log(stock_data / stock_data.shift(1))
retvect = np.matrix((np.mean(ret)*252))


# WEIGHT VECTOR
weights = np.random.rand(len(stocks))
weights /= np.sum(weights)
print('Weights Vector')
print(weights)

# COVARIANCE MATRIX
retcov = np.matrix(ret.cov()*252)
invretcov = np.matrix(retcov).I


# A CALCUATION
A = np.matmul(one, np.matmul(invretcov, np.matrix.transpose(one)))

# B CALCULATION
B = np.matmul(one, np.matmul(invretcov, np.matrix.transpose(retvect)))

# C CALCUALTION
C = np.matmul(retvect, np.matmul(invretcov, np.matrix.transpose(retvect)))

# ∆ CALCULATION
delta = A*C-B**2

# LAMBDA CALCULATION
lammbda = (C-B*target_return)/delta

# GAMMA CALCULATION
gamma = (A*target_return-B)/delta

# OPTIMAL WEIGHTS
optimalweights = np.squeeze(np.asarray(lammbda))*(np.matmul(invretcov, np.matrix.transpose(
    one))) + np.squeeze(np.asarray(gamma))*np.matmul(invretcov, np.matrix.transpose(retvect))
print('Optimal Weights')
print(optimalweights)
