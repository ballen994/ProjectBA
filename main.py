# Import CSV
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import numpy as np
import seaborn as sns
avocado_data = pd.read_csv("avocado.csv")
print(avocado_data.info)
print(avocado_data.shape)
print(avocado_data.dtypes)
avocado_data.Date = pd.to_datetime(avocado_data.Date)
Calavo_SP = pd.read_csv("CVGW.csv")
print(Calavo_SP.info)
print(Calavo_SP.shape)
print(Calavo_SP.dtypes)
Calavo_SP.Date = pd.to_datetime(Calavo_SP.Date)
# Ensure DataFrame is Sorted by time
avocado_data.sort_values('Date', ascending=True,inplace=True)
Calavo_SP.sort_values('Date', ascending=True,inplace=True)
# Merge  on date
# Ensure date datatype on Columns
avocado_data['Date'] = pd.to_datetime(avocado_data['Date'], format='%Y-%m-%d')
Calavo_SP['Date'] = pd.to_datetime(Calavo_SP['Date'], format='%Y-%m-%d')
#Merge Cavalo_SP and avocado_data on Day -1
# Create column with new date
Calavo_SP['date_minus_one'] = Calavo_SP.Date - timedelta(days=1)
avo_and_share = Calavo_SP.merge(avocado_data, how='inner', left_on='date_minus_one', right_on='Date')
print(avo_and_share.info)
print(avo_and_share.shape)
# API for Calavo Growers

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
plt.plot()

# How Many years of Avocado Data in DataFrame
print(avocado_data.Date.dt.strftime('%Y').unique())
# How Many Different Regions are in the Avocado DataFrame?
print('# of Regions:', avocado_data.region.nunique())
# How Many Different Regions are in the Avocado DataFrame?
print('# of Types:', avocado_data.type.unique())
# How Does the Average Price of an Avocado Per Region Compare
average_prices = avocado_data.groupby(['region', 'type']).AveragePrice.mean().reset_index(name='price')
# What is the cheapest and most expensive region (on average over all years) for both Conventional and Organic Avocados
print('\n')
print('Cheapest Region For Avocados')
for avo_type in average_prices.type.unique():
    lowest_price = average_prices[average_prices.type == avo_type].price.min()
    print(avo_type, ':', average_prices[(average_prices.price == lowest_price) &
                                      (average_prices.type == avo_type)
                                             ].region.to_string(index=False))
print('\n')
print('Most Expensive Region For Avocados')

for avo_type in average_prices.type.unique():
    highest_price = average_prices[average_prices.type == avo_type].price.max()
    print(avo_type, ':', average_prices[(average_prices.price == highest_price) &
                                      (average_prices.type == avo_type)
                                             ].region.to_string(index=False))

# How does the price for All US of Convential Avocados compare to Organice
data = avocado_data[avocado_data.region == 'TotalUS'].groupby(['year', 'type']).AveragePrice.mean().reset_index(
    name='price')
data.year = pd.to_datetime(data.year, format='%Y')

data.pivot_table(index='year',columns='type').plot(figsize=(10, 10/1.6))
plt.title('Average Price for all US of Avocados')
plt.ylabel('Price [$]')
plt.xlabel('Year')

# Avocado Prices for the Top 5 Regions Based on Total Volume

region_totals = avocado_data.groupby('region')['Total Volume'].sum()
top5_regions = np.array(region_totals[region_totals.index != 'TotalUS'].sort_values(ascending=False).head(5).index)


plt.figure(figsize=(10,10/1.6))
for region in top5_regions:
    plt.plot(avocado_data[(avocado_data.region == region) &
                         (avocado_data.type == 'conventional')].Date
             ,avocado_data[(avocado_data.region == region) &
                         (avocado_data.type == 'conventional')].AveragePrice,label=region)
plt.legend()
plt.title('Price of Avocado - Top 5 Regions by Total Volume')
plt.ylabel('Price [$]')
plt.show()

# How does the share price of Calavo Correlate with US Price of Avocado

# Make sure the dataframe is sorted by date
avo_and_share.sort_values('Date_x', ascending=True)

fig, ax1 = plt.subplots()
fig.set_size_inches(8, 8/1, 6)
colors = ['r','k']
# Plot On Same Graph with Different Axis
for i,avo_type in enumerate(avo_and_share.type.unique()):

    ax1.plot(avo_and_share[(avo_and_share.region == 'TotalUS') &
                 (avo_and_share.type == avo_type)].Date_x,
             avo_and_share[(avo_and_share.region == 'TotalUS') &
                 (avo_and_share.type == avo_type)].AveragePrice
                         ,colors[i]
             ,label= 'Average Price of an Avocado (Total US)')
    plt.legend(loc='upper left')

ax1.set_ylabel('Average Price of Avocado')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.plot(avo_and_share[(avo_and_share.region == 'TotalUS') &
                 (avo_and_share.type == avo_type)].Date_x,
             avo_and_share[(avo_and_share.region == 'TotalUS') &
                 (avo_and_share.type == avo_type)].Open,label='Opening Share Price'
        ,color='g')
ax2.set_ylabel('Calavo Stock Price')
plt.legend(loc='upper right')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# Create a DataFrame with Avocado Prices and Stock Price to find correlation

data = avo_and_share[avo_and_share.region == 'TotalUS'].pivot_table(index='Date_x',columns='type',values='AveragePrice').reset_index()
data = data.merge(avo_and_share.groupby(['Date_x', 'Open']).size().reset_index().iloc[:, :2], on='Date_x')
data.set_index('Date_x', inplace=True)

f, ax = plt.subplots(figsize=(10, 10/1.6))
sns.heatmap(np.round(data.corr(), 4), annot=True, linewidths=.5, ax=ax)
plt.ylim(0,3)
plt.tight_layout()
plt.show()