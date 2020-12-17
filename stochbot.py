
import talib as ta
import matplotlib.pyplot as plt
plt.style.use('ggplot') #changing to a more visually appealing graph output
import yfinance as yf
import numpy as np
import datetime
import time
import pandas as pd
import math
import bayes_opt


#download function with defaults for XJO, start at 1/1/18 and end today
def dl(ticker = "^AXJO", start_time = datetime.date(2018, 1, 1), end_time = datetime.date.today()):
    df = yf.download(ticker, start = start_time,end = end_time , interval = "1d")
    return df
df = dl(ticker = "APX.AX")
#print(df)

#using TA lib to calculate the slow stochastics of the stock
def slowstochsignal(fastkperiod = 14, slowkperiod = 3, slowkmatype = 0 , slowdperiod = 3, slowdmatype = 0):
    df['slowk'], df['slowd'] = ta.STOCH(df['High'], df['Low'], df['Close'], fastk_period= fastkperiod, 
    slowk_period= slowkperiod, slowk_matype= slowkmatype, slowd_period= slowdperiod, slowd_matype= slowdmatype)
    return df
df = slowstochsignal()
print(df)

def countpotentialbands():
    countb = 0
    counts = 0
    for i, data in df.iterrows():
    #print(df.loc[i,'slowk'])
        if df.loc[i,'slowk'] < 20:
        #print('buy')
            countb += 1
        if df.loc[i,'slowk'] > 80:
            counts += 1
    print("Potential Buy Days:",countb)
    print("Potential Sell Days:",counts)
countpotentialbands()





#start_time = datetime.date(2018, 1, 1)
#end_time = datetime.date.today()
#data = dl()
#print(data)
#print(type(data))
#ticker input
#ticker = "ALU.AX"

#download

#df = yf.download(ticker, start = start_time,end = end_time , interval = "1d")



#df['slowk'], df['slowd'] = ta.STOCH(df['High'], df['Low'], df['Close'], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
#df[['slowk','slowd']].plot(figsize=(15,15))



#df['StochBuy'] = df['slowk'] <= (20) 
#df['StochSell'] = df['slowk'] >= 80 

#df["% change"] = df['Close'].pct_change()
#df['StochBuyBot'] = df['StochBuy']
#df['Bot1'] = 100*(1+df['StochBuy'].shift(1)*df["% change"]).cumprod()
#start_bot1 = df['Bot1'].iloc[14]
#end_bot1 = df['Bot1'].iloc[-1]
#years = (df['Bot1'].count()+1-200)/252
#bot1_average_return = (end_bot1/start_bot1)**(1/years)-1
#df['Hold'] = 100*(1+df['% change']).cumprod()
#print(df)
#print('Buy during <20 fast stochastic oscillator', bot1_average_return*100, '% per year')

#df[['slowk','slowd']].plot(figsize=(15,15))


#df[['Hold','Bot1']].plot(figsize = (15,15))
#plt.show()
#df = df.dopna()




df['buysignal'] = np.where(df['slowk'] < 20, True, False)
df['sellsignal'] = np.where(df['slowk'] > 80, True, False)
df['% change'] = df['Close'].pct_change()
df['stochbuybot'] = 100*(1+df['buysignal'].shift(1)*df['% change']).cumprod()
pd.set_option('display.max_rows', None)


years = (df['Close'].count()+1)/252
start_df = df['Close'].iloc[15]
end_df = df['Close'].iloc[-1]
df_avg_ret = (end_df/start_df)**((1/years)-1)
#print("df average return", df_avg_ret*100, "% per year.")
df['hold'] = 100*(1+df['% change']).cumprod()
#df['hold'].plot(label = "df")
#plt.aihline(y = 20, color = 'darkgreen', linestyle = '-') 
#plt.aihline(y = 15, color = 'green', linestyle = '-') 
#plt.aihline(y = 80, color = 'orangered', linestyle = '-') 
#plt.aihline(y = 85, color = 'red', linestyle = '-')


fig, axs = plt.subplots(2, sharex=True, figsize = (15,15))
fig.suptitle('Stock Price (top) & Slow Stochastics (bottom)')
axs[0].plot(df['Close'], color = 'black')
axs[1].plot(df['slowk'], color = 'black')
axs[1].axhline(y=85, color = "red", linestyle = '-')
axs[1].axhline(y=80, color = "orangered", linestyle = "-")
axs[1].axhline(y=20, color = "darkgreen", linestyle = '-')
axs[1].axhline(y=15, color = "green", linestyle = "-")


df['Long Tomorrow'] = np.nan
df['Buy Signal'] = np.nan
df['Sell Signal'] = np.nan
df['Buy Stoch'] = np.nan
df['Sell Stoch'] = np.nan
df['Strat'] = np.nan



for i in range(15,len(df)):

    if ((df['slowk'][i] <= 20) & (df['slowk'][i-1]>20)):
        df['Long Tomorrow'][i] = True
    elif ((df['Long Tomorrow'][i-1] == True) & (df['slowk'][i] <= 80)):
        df['Long Tomorrow'][i] = True
    else:
        df['Long Tomorrow'][i] = False
    

    #buy signal
    if ((df['Long Tomorrow'][i] == True) & (df['Long Tomorrow'][i-1] == False)):
        df['Buy Signal'][i] = df['Close'][i]
        df['Buy Stoch'][i] = df['slowk'][i]

        
    #calculate "Sell Signal" column
    if ((df['Long Tomorrow'][i] == False) & (df['Long Tomorrow'][i-1] == True)):
        df['Sell Signal'][i] = df['Close'][i]
        df['Sell Stoch'][i] = df['slowk'][i]

        
#calculate strategy performance
df['Strat'][15] = df['Close'][15]

for i in range(16, len(df)):
    if df['Long Tomorrow'][i-1] == True:
        df['Strat'][i] = df['Strat'][i-1]* (df['Close'][i] / df['Close'][i-1])
    else:
        df['Strat'][i] = df['Strat'][i-1]
        
bprices = []
abc = 0
#buy prices:
#for i in range(16, len(df)):
    #if df['Buy Signal'][i] == math.isnan(i) False:
        #prices[i] = df['Close'][i]
        #abc += 1 
for b in df['Buy Signal']:
    if math.isnan(b) == False:
        b = round(b,2)
        bprices.append(b)
sprices = []
for s in df['Sell Signal']:
    if math.isnan(s) == False:
        s = round(s,2)
        sprices.append(s)    
#print(df)
#print("abc",abc)
#print(bprices)
#print(len(bprices))
#print(sprices)
#print(len(sprices))
if len(bprices) > len(sprices):
    bprices = bprices[:(len(bprices)-1)]
dif = np.subtract(sprices,bprices)
#print(dif)


##Chart the buy/sell signals 
plt.style.use('ggplot')
fig, axs = plt.subplots(2, sharex=True, figsize=(13,9))
#title = 'Stock Price (top) & Secret Signal (bottom) for', ticker
#fig.suptitle(title)

#chart the stock close price & buy/sell signals
axs[0].scatter(df.index, df['Buy Signal'],  color = 'green',  marker = '^', alpha = 1)
axs[0].scatter(df.index, df['Sell Signal'],  color = 'red',  marker = 'v', alpha = 1)
axs[0].plot(df['Close'], alpha = 0.8, color = "black")
axs[0].grid()

#chart slowk & buy/sell signals
axs[1].scatter(df.index, df['Buy Stoch'],  color = 'green', marker = '^', alpha = 1)
axs[1].scatter(df.index, df['Sell Stoch'],  color = 'red', marker = 'v', alpha = 1)
axs[1].plot(df['slowk'], alpha = 0.8, color = "black")
axs[1].plot(df['slowd'], alpha = 0.3, color = "blue")
axs[1].grid()


##some performance statistics
#calculate the number of trades
trade_count = df['Buy Signal'].count()

#calculate the average profit per trade
average_profit = ((df['Strat'][-1] / df['Strat'][15])**(1/trade_count))-1

#calculate the average # of days per trade
total_days = df['Long Tomorrow'].count()
average_days = int(total_days / trade_count)

#print('This strategy yielded ', trade_count, ' trades')
#print('The average trade lasted ', average_days, ' days per trade')
#print('The average profit per trade was ', average_profit*100, '%')


plt.show()

#testing github linkage

