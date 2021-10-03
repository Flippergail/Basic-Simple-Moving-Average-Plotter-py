# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2020-01-01', '2021-01-01')
moving_average = data['Adj Close'].rolling(window=20).mean()
# initializing the short and long lookback periods
short_lb = 10
mid_lb = 18
long_lb = 35
# initializing a new DataFrame called signal_df with a signal column
signal_df = pd.DataFrame(index=data.index)
signal_df['long_signal'] = 0.0
signal_df['mid_signal'] = 0.0
signal_df['profit'] = 0.0
# making moving averages over time periods
signal_df['short_mav'] = data['Adj Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
signal_df['mid_mav'] = data['Adj Close'].rolling(window=mid_lb, min_periods=1, center=False).mean()
signal_df['long_mav'] = data['Adj Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
signal_df['actual_price'] = data['Adj Close']
# generates the signals based on the conditional statement
signal_df['long_signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)
signal_df['mid_signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['mid_mav'][short_lb:], 1.0, 0.0)
# creating the trading orders based on the positions column
signal_df['long_positions'] = signal_df['long_signal'].diff()
signal_df['mid_positions'] = signal_df['mid_signal'].diff()
signal_df[signal_df['long_positions'] == -1.0]
signal_df[signal_df['mid_positions'] == -1.0]
# initialize the plot using plt
fig = plt.figure()
# Add a subplot and label for y-axis
plt1 = fig.add_subplot(111,  ylabel='Price in $')
data['Adj Close'].plot(ax=plt1, color='r', lw=2.)
# plot the short and long lookback moving averages
signal_df[['short_mav', 'mid_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
print(signal_df)
# plotting the sell/buy signals
long_sell = signal_df.loc[signal_df.long_positions == -1.0].index
long_buy = signal_df.loc[signal_df.long_positions == 1.0].index
mid_sell = signal_df.loc[signal_df.mid_positions == -1.0].index
mid_buy = signal_df.loc[signal_df.mid_positions == 1.0].index
plt1.plot(long_buy, signal_df.actual_price[signal_df.long_positions == 1.0], 'h', markersize=8, color='c')
plt1.plot(long_sell, signal_df.actual_price[signal_df.long_positions == -1.0], 'h', markersize=8, color='y')
plt1.plot(mid_buy, signal_df.actual_price[signal_df.mid_positions == 1.0], 'D', markersize=7, color='g')
plt1.plot(mid_sell, signal_df.actual_price[signal_df.mid_positions == -1.0], 'D', markersize=7, color='m')
plt.show()