# CI Bot

import sqlite3
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd

conn = sqlite3.connect('stockdatabase.db')
c = conn.cursor()
c.execute("SELECT Adj_Close FROM 'stock_table_BHP.AX' WHERE ROWID >= 2526")
data = c.fetchall()
c.close()
conn.close()

df = pd.DataFrame(data)
print(df)
mu = np.average(df[0])
std = np.std(df[0])
n = len(df[0])
#df['MA'] = df[0].rolling(window=15).mean()
#df['RSTD'] = df[0].rolling(window=15).std()


#rolling_mean = df.rolling(10).mean()
#rolling_std = df.rolling(10).std()

#df['Bollinger High'] = df['MA'] + (df['RSTD'] * 1.64)
#df['Bollinger Low'] = df['MA'] - (df['RSTD'] * 1.64)
#
df['Bollinger High'] = df[0].rolling(
    window=15).mean() + (df[0].rolling(window=15).std()*1.5)
df['Bollinger Low'] = df[0].rolling(
    window=15).mean() - (df[0].rolling(window=15).std()*1.5)

plt.plot(df[0].rolling(window=15).mean())
plt.plot(df['Bollinger High'], color='r')
plt.plot(df['Bollinger Low'], color='r')
plt.plot(data)
plt.show()
