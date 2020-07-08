import time
import datetime
import yfinance as yf
import sqlite3
import pandas as pd

""" list = ['CBA', 'BHP','RIO','ANZ', 'WTC']
for each in list:
    AXJO = yf.Ticker(each + ".AX") """


def yfsqldownload(ticker):
    start_time = datetime.date(2010, 1, 1)
    end_time = datetime.date.today()
    setinterval = "1d"

    data = yf.download(tickers=ticker, start=start_time, end=end_time,
                       group_by="ticker", interval=setinterval)  # ['Adj Close']
    # Feature of yfinance is the data downloads in a dataframe

    if isinstance(data, pd.DataFrame):
        print("Data download is a dataframe")
    elif isinstance(data, pd.DataFrame):
        print("Data download is not a dataframe")
    # Checking if the yahoofinance download is a dataframe

    data.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
    # Renaming a column so it is more SQL friendly
    tickerID = []
    for i in range(len(data)):
        tickerID.append(ticker)
    data['Ticker'] = tickerID
    # Adding a stock ID to the dataframe

    data = data.reset_index()
    # Resetting the index from date to numbers so it is more friendly to SQL
    # print(data)

    conn = sqlite3.connect('stockdatabase.db')
    c = conn.cursor
    data.to_sql('stock_table_'+ticker, con=conn,
                if_exists='append', index=True)
    conn.commit()
    conn.close()


list = ['CBA.AX', 'RIO.AX', 'MQG.AX']
for i in list:
    yfsqldownload(i)

# yfsqldownload('RIO.AX')

""" # SQL Part
conn = sqlite3.connect('stockdb.db')
c = conn.cursor
data.to_sql('stock_table', con=engine, if_exists='replace', index=True)

print('printing results of the SELECT statement: ')
print(" ") 
select_statement = 'SELECT * FROM stockdb WHERE Adj_Close > 270.0;'
cur.execute(select_statement)
for line in cur.fetchall():
    print(line)
 
 cur.close()
engine.close() 
 """
# https://docs.python.org/3/library/sqlite3.html
# https://pythontic.com/modules/sqlite/introduction
# https://www.youtube.com/watch?v=NCc5r7Wr7gg
