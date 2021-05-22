# Import CSV
import pandas as pd
avocado_data = pd.read_csv("avocado.csv")
print(avocado_data)

# API for Calavo Growers
import requests
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
API_key = '7Y32JGC45LCIARCK'
ts = TimeSeries(key=API_key, output_format='pandas')
stock_data, meta = ts.get_intraday('CVGW', interval='1min', outputsize='compact')
columns = ['open', 'high', 'low', 'close', 'volume']
stock_data.columns = columns
stock_data['TradeDate'] = stock_data.index.date
stock_data['Time'] = stock_data.index.time
print(stock_data)
print(stock_data['close'])
end_of_day_info = (stock_data.iloc[0:1, 0:5])
print(end_of_day_info)
print(end_of_day_info['close'])

# Plot a graph to visualise the above movement in share price
plt.plot(stock_data['close'], lw=.5, linestyle='-')
plt.xlabel('Time and Date', fontsize=15, fontweight='bold')
plt.ylabel('$USD', fontsize=15, fontweight='bold')
plt.title('Stock Price over last 100 minutes', fontsize=25, fontweight='bold')
plt.show()



