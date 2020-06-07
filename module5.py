import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

stocks = ['EOS.AX']
data = yf.download(tickers="EOS.AX",
                   start="2015-01-01", group_by="ticker", interval="1d")  # ['Adj Close']


print(data)
close = data['Adj Close']
plt.figure(1)
plt.plot(close)
plt.ylabel('Stock price in $')

plt.figure(2)
rets1 = np.log(close / close.shift(1))
rets1 = rets1[2:len(rets1)]
rets = data['Adj Close'].pct_change()
rets = rets[~np.isnan(rets)]
plt.plot(rets)


plt.figure(3)
bins = 100
plt.hist(rets1, bins)


data_market = yf.download(tickers="XJO.AX",
                          start="2015-01-01", group_by="ticker", interval="1d")  # ['Adj Close']

marketclose = data_market['Adj Close']
marketrets1 = np.log(marketclose / close.shift(1))
marketrets1 = marketrets1[2:len(marketrets1)]
marketrets = data_market['Adj Close'].pct_change()
marketrets = marketrets[~np.isnan(rets)]
plt.figure(4)
plt.scatter(marketrets, rets)
plt.show()
