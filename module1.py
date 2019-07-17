# Module 1 Risk and Return of an Individual Asset
import fix_yahoo_finance as yf
import pandas_datareader.data as pdr
import numpy as np

print("Individual Asset Risk and Return")
print('Exchanges to Choose From:')
xc = ['.AX', '.NYSE']
print(xc)
print('Choose your exchange...')
exchange = input()
print('Enter your ' + exchange + ' stock....')
stock = input() + exchange

exchange_code = "^AXJO"

exchange_data = pdr.get_data_yahoo(exchange_code)['Adj Close']
stock_data = pdr.get_data_yahoo(stock)['Adj Close']

# Beta Calculation
# beta asset = cov (asset return and market return ) / market variance
exchange_variance = int(
    mean(np.log(exchange_data / exchange_data.shift(1)))*252)
stock_return = mean(np.log(stock_data / stock_data.shift(1)))*252)
covariance=cov(exchange_return, stock_return)
exchange_variance=var(exchange_data)
asset_beta=covariance / exchange_variance
Print("The beta of the asset is:" + asset_beta)


Print('Are you finished?')
menu_status=input()
if menu_status=["yes", 'Yes', 'ye', 'eys']:
    import menus
