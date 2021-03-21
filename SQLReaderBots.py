#Stochatic Bot w local MySQL
import mysql.connector
import pandas as pd
import talib as ta
import numpy as np
import operator 
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#login credentials
my_connect = mysql.connector.connect(
    host = "",
    user = '',
    passwd = "",
    database = ""
)
#selecting an equity from the database
inputstr = 'msft'
query = "SELECT * FROM "+inputstr
df = pd.read_sql(query, my_connect)
df['date'] = pd.to_datetime(df['Date']).dt.date

#introducing the fear greed index signal
df1 = pd.read_sql("SELECT * FROM cnnfgifull", my_connect)

#setting the plot style to use with matplotlib
plt.style.use('ggplot')



def slowstochsignal(fastkperiod = 14, slowkperiod = 3, slowkmatype = 0 , slowdperiod = 3, slowdmatype = 0):
    df['slowk'], df['slowd'] = ta.STOCH(df['High'], df['Low'], df['Close'], fastk_period= fastkperiod, 
    slowk_period= slowkperiod, slowk_matype= slowkmatype, slowd_period= slowdperiod, slowd_matype= slowdmatype)
    return df
df = slowstochsignal()

def sma(timeperiod = 50):
    df['sma'] = ta.SMA(df['Close'], timeperiod)
    return df
df = sma()

def rsi(timeperiod = 14):
    df['rsi'] = ta.RSI(df['Close'], timeperiod)
    return df
df = rsi()

def roc(timeperiod = 14):
    df['roc'] = ta.ROC(df['Close'], timeperiod)
    return df
df = roc()

def adosc(fastperiod = 3, slowperiod = 10):
    df['adosc'] = ta.ADOSC(df['High'], df['Low'], df['Close'], df['Volume'], fastperiod, slowperiod)
    return df
df = adosc()

def bb(timeperiod=5, nbdevup = 2, nbdevdn = 2, matype = 0):
    df['upperband'], df['middleband'], df['lowerband'] = ta.BBANDS(df['Close'], timeperiod, nbdevup, nbdevdn, matype)
    return df
df = bb()




def countpotentialmoves(lowerbound = 20, upperbound = 80):
    countb = 0
    counts = 0
    for i, data in df.iterrows():
    #print(df.loc[i,'slowk'])
        if df.loc[i,'slowk'] < 20:
        #print('buy')
            countb += 1

            #df['Buy Stoch'][i] = df['slowk'][i]
        if df.loc[i,'slowk'] > 80:
            counts += 1
            
    #df['bb'] = np.where(df['slowk'] < lowerbound, True, False)
    #df['ss'] = np.where(df['slowk'] > upperbound, True, False)
    print("Potential Buy Days:",countb)
    print("Potential Sell Days:",counts)
#countpotentialmoves()



df['Buy Signal'] = np.nan
df['Sell Signal'] = np.nan
df['Buy Stoch'] = np.nan
df['Sell Stoch'] = np.nan
df['Strat'] = np.nan
df['bb'] = np.nan
df['ss'] = np.nan
df['bstoch'] = np.nan
df['sstoch'] = np.nan
df['buysmacross'] = np.nan

df['OpenPosition'] = False


def slowstochasticalltrades(lowerband, upperband):
    for i, data in df.iterrows():
        if df.loc[i,'slowk'] <= lowerband:
            df.loc[i,'bb'] = df.loc[i,'Close']
            df.loc[i,'bstoch'] = df.loc[i,'slowk']
        elif df.loc[i,'slowk'] >= upperband:
            df.loc[i,'ss'] = df.loc[i,'Close']
            df.loc[i,'sstoch'] = df.loc[i,'slowk']
slowstochasticalltrades(20,90)

def slowstochastictrades1(lowerband, upperband):
    for i, data in df.iterrows():
        if (df.loc[i,'OpenPosition'] == False) & (df.loc[i,'slowk'] <= lowerband):
            (df.loc[i+1,'OpenPosition'] == True)
            print(df.loc[i,'Close'])
            print("Opened Position")
#slowstochastictrades(20,90)



buys = []
sells = []
def slowstochastictrades2(lowerband, upperband):
    flag = 0
    for i, data in df.iterrows():   
        if (flag == 0) & (df.loc[i,'slowk'] <= lowerband):
            flag = 1
            #print(df.loc[i,'Close'])
            #print("Opened Position")
            buys.append(df.loc[i,'Close'])
        if (flag == 1) & (df.loc[i,'slowk'] >= upperband):
            flag = 0 
            #print(df.loc[i,'Close'])
            #print('Closed Position')
            sells.append(df.loc[i,'Close'])
    #print(buys)
    #print(sells)
    profit = list(map(operator.sub, sells, buys))
    #print(profit)
    cumulativelist = []
    cumulative = 0 
    for j in profit:
        cumulative += j 
        cumulativelist.append(cumulative)  
    cumulativelist = [round(n,2) for n in cumulativelist]
    print("Profit:",round(cumulative,2))
    #print(cumulativelist)
    #cumulativeprofits = plt.figure(1)
    plt.title("Cumulative Profit Per Share")
    plt.plot(cumulativelist, color = 'green')
    return cumulativelist

    
slowstochastictrades2(20,80)



def slowstochastictrades3(lowerband, upperband):
    #intiating the lists for which the buy and sell prices are stored in.
    buys1 = []
    sells1 = []
    #flag = 0 no trades open, flag = 1 position currently open
    flag = 0 
    for i, data in df.iterrows():
        if (flag == 0) & (df.loc[i,'slowk'] <= lowerband):
            flag = 1
            buys1.append(df.loc[i,'Close'])
        if (flag == 1) & (df.loc[i, 'slowk'] >= upperband):
            flag = 0 
            sells1.append(df.loc[i,'Close'])
    profit = list(map(operator.sub, sells1, buys1))
    cumulativelist = []
    cumulative = 0
    for j in profit:
        cumulative += j
        cumulativelist.append(cumulative)
    cumulativelist = [round(n,2) for n in cumulativelist]
    cumulativeprofit = round(cumulative,2)
    return cumulativeprofit
print(slowstochastictrades3(20,80))
print("break")


xcoordinates = []
ycoordinates = []
zcoordinates = [] 
for ii in range(20,25):
    for ij in range(80,85):
        xcoordinates.append(ii)
        ycoordinates.append(ij)
        z = slowstochastictrades3(ii,ij)
        zcoordinates.append(z)
        #print(slowstochastictrades3(ii, ij))


coords = pd.DataFrame(list(zip(xcoordinates, ycoordinates, zcoordinates)), columns =['x', 'y', 'z']) 
#print(coords)
coordsordered = pd.DataFrame(coords.sort_values(by='z', ascending = False))
# coordsordered = pd.DataFrame(coordsordered)
coordsordered = coordsordered.reset_index(drop = True)
#print("Ordered by most profitable levels first")
#print(coordsordered)
# print(coordsordered.head())
optimumx = coordsordered.at[0,'x']
optimumy = coordsordered.at[0,'y']


plotx,ploty = np.meshgrid(np.linspace(np.min(xcoordinates), np.max(xcoordinates),10),\
    np.linspace(np.min(ycoordinates),np.max(ycoordinates),10))
plotz = interp.griddata((xcoordinates,ycoordinates),zcoordinates,(plotx,ploty), method ='linear')
slippageregion = (plotx - optimumx)**2+(ploty - optimumy)**2 - 9 


fig = plt.figure(10)
ax = fig.add_subplot(111,projection = '3d')

ax.plot_surface(plotx,ploty,plotz,cstride = 1, rstride = 1, cmap = 'viridis') #hot, cool, etc

ax.set_xlabel('Lower Bound')#, fontsize=20, rotation=150)
ax.set_ylabel('Upperbound Bound')#, fontsize=20, rotation=150)
ax.set_zlabel('Profit per Share')#, fontsize=20, rotation=150)
ax.set_title(inputstr + " optimisation graph for Slow Stochastic TA")
#ax.scatter(coordsordered.loc[0,0], coordsordered[0,1], coordsordered[0,2], color='k', label='Your guess at constrained maximum')
ax.scatter(coordsordered.at[0,'x'], coordsordered.at[0,'y'], coordsordered.at[0,'z'], color='k', label='Your guess at constrained maximum')


#if df['p'][i] & df['p-1'][i] & df['p-2'][i] == True:



def smabot():
    for i,data in df.iterrows():
        if df.loc[i,'Close'] <= df.loc[i,'sma']:
            df.loc[i,'buysmacross'] = df.loc[i,'Close'] 
smabot()


df['dailyrets'] = df['Adj Close'].pct_change()
#dailyrets = dailyrets[~np.isnan(dailyrets)]
bins = 100
#fig2, axs = plt.subplots(1,1)
#axs[0].hist(dailyrets,bins)
rets = plt.figure(2)
plt.hist(df['dailyrets'], bins)

eco = plt.figure(3)
plt.plot(df['Date'], df['dailyrets'], scalex= True, scaley = True)

def plotting():
    #charting all potential moves
    fig1, axs1 = plt.subplots(8, sharex=True, figsize = (13,9))
    fig1.suptitle('Stock Price (top) & Slow Stochastics (bottom)')
    #plt.xlabel('date')
    axs1[0].scatter(df['Date'], df['bb'], color = 'green', marker = "^", alpha = 1)
    axs1[0].scatter(df['Date'], df['ss'], color = 'red', marker = "v", alpha = 1)
    
    axs1[0].plot(df['Date'],df['Close'], color = 'black')
    axs1[0].plot(df['Date'], df['sma'], color = 'blue', alpha = 0.8)

    axs1[1].scatter(df['Date'], df['bstoch'], color = 'green', marker = "^", alpha = 1)
    axs1[1].scatter(df['Date'], df['sstoch'], color = 'red', marker = "v", alpha = 1)
    axs1[1].plot(df['Date'],df['slowk'], alpha = 0.8, color = "black")
    #plt.show()
    axs1[2].plot(df1['Date'], df1['today'], color = 'blue', alpha = 1)

    axs1[3].plot(df['Date'], df['rsi'], color = 'black')
    axs1[3].set_title('RSI', loc = 'center')
    axs1[3].axhline(y = 30, color = 'red')
    axs1[3].axhline(y = 70, color = 'green')
    axs1[3].fill_between(df['Date'], 0, 30,color='red', alpha=0.2)
    axs1[3].fill_between(df['Date'], 70,100, color = 'green', alpha = 0.2)
    axs1[4].plot(df['Date'], df['roc'], color = 'black')

    axs1[5].set_title('MA Cross', loc = 'center')
    axs1[5].scatter(df['Date'], df['buysmacross'], color = 'purple', marker = "^", alpha = 1)
    axs1[5].plot(df['Date'], df['sma'], color = 'blue', alpha = 0.6)
    axs1[5].plot(df['Date'], df['Close'], color = 'black')

    axs1[6].plot(df['Date'], df['dailyrets'], color = 'black')


    axs1[7].plot(df['Date'], df['Close'], color = 'black')
    axs1[7].plot(df['Date'], df['upperband'], color = 'red')
    axs1[7].plot(df['Date'], df['middleband'])
    axs1[7].plot(df['Date'], df['lowerband'], color = 'red')

    
plotting()
plt.show()




