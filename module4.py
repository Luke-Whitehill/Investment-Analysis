# MODULE 4 - Recents
import fix_yahoo_finance as yf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr

yf.pdr_override()

exchange = '.AX'
print('Enter your ' + exchange + ' stock....')
stock = input() + exchange
while stock != 'Exit':
    recent_history = pdr.get_data_yahoo(stock)
    print(recent_history.tail())
    recent_history.tail()['Adj Close'].plot()
    plt.title('Share Price vs Date')
    plt.ylabel('Return')
    plt.xlabel('Date')
    plt.show()
    print('Enter your ' + exchange + ' stock....')
    stock = input() + exchange

# Notes: Make it so its not just recent, graph it in mpl etc evolve into technical analysis. Learn from tkinter?
print("It's been a while since I did any python programming :( ")
