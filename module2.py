#MODULE 3 - Markowitz
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import math as math
yf.pdr_override()

exchange = '.AX'
tickers = ['MQG.AX', 'CBA.AX', 'WOW.AX']
noa = len(tickers)

data = pd.DataFrame()
for ticker in tickers:
    data[ticker] = pdr.get_data_yahoo(ticker)['Adj Close']

rets = np.log(data / data.shift(1))
rets.hist(bins = 40, figsize=(10,8))
retsmean = rets.mean() * 252
retscov = rets.cov() * 252

weights = np.random.random(noa)
weights /= np.sum(weights)
print('Return of the asset')
print(retsmean)
retsp = np.sum(rets.mean() * weights) * 252
varp = np.dot(weights.T, np.dot(rets.cov() * 252, weights))


def port_ret(weights):
    return np.sum(rets.mean() * weights) * 252

def port_vol(weights):
    return np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
#Portfolio Randomiser, Monte Carlo
prets = []
pvols = []
for p in range (2500):
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    prets.append(port_ret(weights))
    pvols.append(port_vol(weights))

prets = np.array(prets)
pvols = np.array(pvols)


#Minimisation
import scipy.optimize as sco
def min_func_sharpe(weights):
    return -port_ret(weights) / port_vol(weights)

cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) -1})
bnds = tuple((0,1) for x in range(noa))
eweights = np.array(noa * [1. / noa,])
min_func_sharpe(eweights)
print('Optimal Weights')
print(eweights)

opts = sco.minimize(min_func_sharpe, eweights, method ='SLSQP', bounds=bnds, constraints = cons)

opts['x'].round(3)
port_ret(opts['x']).round(3)
port_vol(opts['x']).round(3)
port_ret(opts['x']) / port_vol(opts['x'])

optv = sco.minimize(port_vol, eweights, method = 'SLSQP', bounds = bnds, constraints = cons)
optv['x'].round(3)
port_ret(optv['x']).round(3)
port_vol(optv['x']).round(3)
port_ret(optv['x']) / port_vol(optv['x'])

#Efficient Frontier
cons = ({'type': 'eq', 'fun': lambda x: port_ret(x) - tret},
{'type':'eq', 'fun':lambda x: np.sum(x) - 1})

bnds = tuple((0,1) for x in weights)

trets = np.linspace(0.05, 0.2, 50)
tvols = []
for tret in trets:
    res = sco.minimize(port_vol, eweights, method = 'SLSQP', bounds = bnds, constraints = cons)
    tvols.append(res['fun'])
tvols = np.array(tvols)


plt.figure(figsize=(10, 6))
plt.scatter(pvols, prets, c=prets / pvols, marker='o', cmap='coolwarm')
plt.plot(port_vol(opts['x']), port_ret(opts['x']), 'b*', markersize = 15.0)
plt.plot(port_vol(optv['x']), port_ret(optv['x']), 'r*', markersize = 15.0)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')
plt.show()
