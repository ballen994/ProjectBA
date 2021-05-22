# API
import requests
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
API_key = '7Y32JGC45LCIARCK'
ts = TimeSeries(key=API_key, output_format='pandas')
stock_data, meta = ts.get_intraday('F', interval='15min',)
columns = ['open', 'high', 'low', 'close', 'volume']
stock_data.columns = columns
stock_data['TradeDate'] = stock_data.index.date
stock_data['Time'] = stock_data.index.time
print(stock_data['close'])
plt.plot(stock_data['close'], lw=6, linestyle='-')
plt.xlabel('Time and Date', fontsize=15, fontweight='bold')
plt.ylabel('$USD', fontsize=15, fontweight='bold')
plt.title('Up to date Stock Price', fontsize=25, fontweight='bold')
plt.show()
