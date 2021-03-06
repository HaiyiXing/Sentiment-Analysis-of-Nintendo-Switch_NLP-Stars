from yahoofinancials import YahooFinancials
from datetime import date, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# get stock ticker symbol from user
stock_symbol = 'NTDOY'

# set date range for historical prices
end_time = date.today()
start_time = end_time - timedelta(days=365)

# reformat date range
end = end_time.strftime('%Y-%m-%d')
start = start_time.strftime('%Y-%m-%d')

# get prices
json_prices = YahooFinancials(stock_symbol
    ).get_historical_price_data(start, end, 'daily')

# transform json file to dataframe
prices = pd.DataFrame(json_prices[stock_symbol]
    ['prices'])[['formatted_date', 'close']]

# sort dates in descending order
prices.sort_index(ascending=False, inplace=True)

# calculate daily logarithmic return
prices['returns'] = (np.log(prices.close / 
    prices.close.shift(-1)))