# Module 1 Risk and Return of an Individual Asset
import fix_yahoo_finance as yf
import pandas_datareader.data as pdr

print("Individual Asset Risk and Return")
print('Exchanges to Choose From:')
xc = ['.AX', '.NYSE']
print(xc)
print('Choose your exchange...')
exchange = input()
print('Enter your ' + exchange + ' stock....')
stock = input() + exchange

exchange_code = "^AXJO"


def history(stock):
    recent_history = pdr.get_data_yahoo(stock)
    print(recent_history.tail())


history(stock)
