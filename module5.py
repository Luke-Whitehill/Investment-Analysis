# from Database import yfsqldownload
from scipy.stats import norm
import math
import scipy.stats as stats
from scipy import stats
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import sqlite3

stocks = ['EOS.AX']
data = yf.download(tickers="IAG.AX", start="2018-03-30",
                   group_by="ticker", interval="1d")  # ['Adj Close']


# print(data)
# Stock Price Graph
close = data['Adj Close']
plt.subplot(2, 1, 1)
plt.plot(close)
plt.ylabel('Stock price in $')
# print(close)

# Daily Returns graph - think Time Series Econometrics
plt.subplot(2, 1, 2)
# rets1 = np.log(close / close.shift(1))
# rets1 = rets1[2:len(rets1)]
rets = data['Adj Close'].pct_change()
rets = rets[~np.isnan(rets)]
rets = np.array(rets)
print('Returns without dates')
print(rets)
# retciupr = np.average(rets)+1.96*(np.std(rets)/len(rets))
mu = np.average(rets)
std = np.std(rets)
n = len(rets)
cilwr = mu+1.96*std*np.sqrt(1+1/n)
ciupr = mu-1.96*std*np.sqrt(1+1/n)
# upr = (np.average(rets))+1.96*(np.std(rets)*np.sqrt(1+(1/len(rets)))
# retcilwr = np.average(rets)-1.96*(np.std(rets)/len(rets))
# lwr=(np.average(rets))-(1.96*(np.std(rets)*np.sqrt(1+(1/len(rets)))))
# retcilwr=(np.average(rets))-1.96*(np.std(rets)*sqrt(1+(1/lenght(rets)))
plt.axhline(y=cilwr, color='r', linestyle="-")
plt.axhline(y=ciupr, color='r', linestyle="-")
plt.plot(rets)


# plt.figure(3)
# plt.plot(retciupr)
# plt.plot(retcilwr)

# Fit a normal distribution to the data:
mu, std = norm.fit(rets)

# Plot the histogram.

plt.figure(2)
plt.hist(rets, bins=100, density=True, alpha=0.6, color='b')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()


""" plt.figure(4)
# The variable 'rets1' will be our histogram plotting variable.

# Fit a normal distribution to the data:
mu, std = norm.fit(rets1)
# Plot histogram
plt.hist(rets1, bins, density=True)
# Plotting the PDF
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f, std = %.2f" % (mu, std)
plt.title(title)
plt.show() """


# data_market = yf.download(tickers="^AORD", start = "2015-01-01", group_by = "ticker", interval = "1d")  # ['Adj Close']
# marketret = data_market['Adj Close'].pct_change()
# marketret = marketret[~np.isnan(marketret)]
# print(marketret)


""" plt.figure(4)
plt.scatter(marketret, rets)
plt.show()
corr = stats.pearsonr(marketret, rets)
print(corr[0]) """


# yfsqldownload('BHP.AX')


# fetching data from sql database
conn = sqlite3.connect('stockdatabase.db')
c = conn.cursor()
select_statement = "SELECT Adj_Close FROM 'stock_table_BHP.AX'"
c.execute(select_statement)
rows = c.fetchall()
# for row in rows:
# print(row)
c.close()
conn.close()

plt.plot(rows)
plt.show()
