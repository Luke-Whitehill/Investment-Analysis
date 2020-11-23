import talib as ta
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import yfinance as yf
ticker = "MQG.AX"
aapl = yf.download(ticker, '2017-11-6','2020-11-20', interval = "1d")
import numpy as np

aapl['slowk'], aapl['slowd'] = ta.STOCH(aapl['High'], aapl['Low'], aapl['Close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
#aapl[['slowk','slowd']].plot(figsize=(15,15))



#aapl['StochBuy'] = aapl['slowk'] <= (20) 
#aapl['StochSell'] = aapl['slowk'] >= 80 

#aapl["% change"] = aapl['Close'].pct_change()
#aapl['StochBuyBot'] = aapl['StochBuy']
#aapl['Bot1'] = 100*(1+aapl['StochBuy'].shift(1)*aapl["% change"]).cumprod()
#start_bot1 = aapl['Bot1'].iloc[14]
#end_bot1 = aapl['Bot1'].iloc[-1]
#years = (aapl['Bot1'].count()+1-200)/252
#bot1_average_return = (end_bot1/start_bot1)**(1/years)-1
#aapl['Hold'] = 100*(1+aapl['% change']).cumprod()
#print(aapl)
#print('Buy during <20 fast stochastic oscillator', bot1_average_return*100, '% per year')

#aapl[['slowk','slowd']].plot(figsize=(15,15))


#aapl[['Hold','Bot1']].plot(figsize = (15,15))
#plt.show()
#aapl = aapl.dopna()
countb = 0
counts = 0
for i, data in aapl.iterrows():
    #print(aapl.loc[i,'slowk'])
    if aapl.loc[i,'slowk'] < 20:
        #print('buy')
        countb += 1
    if aapl.loc[i,'slowk'] > 80:
        counts += 1

print("buy count:",countb)
print("sell count: ",counts)



aapl['buysignal'] = np.where(aapl['slowk'] < 20, True, False)
aapl['sellsignal'] = np.where(aapl['slowk'] > 80, True, False)
aapl['% change'] = aapl['Close'].pct_change()
aapl['stochbuybot'] = 100*(1+aapl['buysignal'].shift(1)*aapl['% change']).cumprod()
print(aapl.head())

years = (aapl['Close'].count()+1)/252
start_aapl = aapl['Close'].iloc[15]
end_aapl = aapl['Close'].iloc[-1]
aapl_avg_ret = (end_aapl/start_aapl)**((1/years)-1)
print("AAPL average return", aapl_avg_ret*100, "% per year.")
aapl['hold'] = 100*(1+aapl['% change']).cumprod()
#aapl['hold'].plot(label = "AAPL")
#plt.aihline(y = 20, color = 'darkgreen', linestyle = '-') 
#plt.aihline(y = 15, color = 'green', linestyle = '-') 
#plt.aihline(y = 80, color = 'orangered', linestyle = '-') 
#plt.aihline(y = 85, color = 'red', linestyle = '-')


fig, axs = plt.subplots(2, sharex=True, figsize = (15,15))
fig.suptitle('Stock Price (top) & Slow Stochastics (bottom)')
axs[0].plot(aapl['Close'], color = 'black')
axs[1].plot(aapl['slowk'], color = 'black')
axs[1].axhline(y=85, color = "red", linestyle = '-')
axs[1].axhline(y=80, color = "orangered", linestyle = "-")
axs[1].axhline(y=20, color = "darkgreen", linestyle = '-')
axs[1].axhline(y=15, color = "green", linestyle = "-")


aapl['Long Tomorrow'] = np.nan
aapl['Buy Signal'] = np.nan
aapl['Sell Signal'] = np.nan
aapl['Buy Stoch'] = np.nan
aapl['Sell Stoch'] = np.nan
aapl['Strat'] = np.nan

for i in range(15,len(aapl)):

    if ((aapl['slowk'][i] <= 20) & (aapl['slowk'][i-1]>20)):
        aapl['Long Tomorrow'][i] = True
    elif ((aapl['Long Tomorrow'][i-1] == True) & (aapl['slowk'][i] <= 90)):
        aapl['Long Tomorrow'][i] = True
    else:
        aapl['Long Tomorrow'][i] = False
    

    #buy signal
    if ((aapl['Long Tomorrow'][i] == True) & (aapl['Long Tomorrow'][i-1] == False)):
            aapl['Buy Signal'][i] = aapl['Close'][i]
            aapl['Buy Stoch'][i] = aapl['slowk'][i]
        
    #calculate "Sell Signal" column
    if ((aapl['Long Tomorrow'][i] == False) & (aapl['Long Tomorrow'][i-1] == True)):
        aapl['Sell Signal'][i] = aapl['Close'][i]
        aapl['Sell Stoch'][i] = aapl['slowk'][i]
        
#calculate strategy performance
aapl['Strat'][15] = aapl['Close'][15]

for i in range(16, len(aapl)):
    if aapl['Long Tomorrow'][i-1] == True:
        aapl['Strat'][i] = aapl['Strat'][i-1]* (aapl['Close'][i] / aapl['Close'][i-1])
    else:
        aapl['Strat'][i] = aapl['Strat'][i-1]
        
print(aapl)


##Chart the buy/sell signals 
plt.style.use('ggplot')
fig, axs = plt.subplots(2, sharex=True, figsize=(13,9))
title = 'Stock Price (top) & Secret Signal (bottom) for', ticker
fig.suptitle(title)

#chart the stock close price & buy/sell signals
axs[0].scatter(aapl.index, aapl['Buy Signal'],  color = 'green',  marker = '^', alpha = 1)
axs[0].scatter(aapl.index, aapl['Sell Signal'],  color = 'red',  marker = 'v', alpha = 1)
axs[0].plot(aapl['Close'], alpha = 0.8, color = "black")
axs[0].grid()

#chart slowk & buy/sell signals
axs[1].scatter(aapl.index, aapl['Buy Stoch'],  color = 'green', marker = '^', alpha = 1)
axs[1].scatter(aapl.index, aapl['Sell Stoch'],  color = 'red', marker = 'v', alpha = 1)
axs[1].plot(aapl['slowk'], alpha = 0.8, color = "black")
axs[1].grid()


##some performance statistics
#calculate the number of trades
trade_count = aapl['Buy Signal'].count()

#calculate the average profit per trade
average_profit = ((aapl['Strat'][-1] / aapl['Strat'][15])**(1/trade_count))-1

#calculate the average # of days per trade
total_days = aapl['Long Tomorrow'].count()
average_days = int(total_days / trade_count)

print('This strategy yielded ', trade_count, ' trades')
print('The average trade lasted ', average_days, ' days per trade')
print('The average profit per trade was ', average_profit*100, '%')


plt.show()

#testing github linkage

