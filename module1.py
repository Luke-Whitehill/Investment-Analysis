# Module 1 Risk and Return of an Individual Asset
import fix_yahoo_finance as yf
import pandas_datareader.data as pdr

print("Individual Asset Risk and Return")
exchange = '.AX'
exchange_code = "^AXJO"
print('Enter your ' + exchange + ' stock....')
stock = input() + exchange


def history(stock):
    recent_history = pdr.get_data_yahoo(stock)
    print(recent_history.tail())


history(stock)
