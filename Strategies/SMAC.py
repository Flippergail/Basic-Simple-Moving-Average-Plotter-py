# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2018-09-01', '2021-09-01')
moving_average = data['Adj Close'].rolling(window=20).mean()
# initializing the short and long lookback periods
short_lb = 50
long_lb = 120
# initializing a new DataFrame called signal_df with a signal column
signal_df = pd.DataFrame(index=data.index)
signal_df['signal'] = 0.0
# making moving averages over time periods
signal_df['short_mav'] = data['Adj Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
signal_df['long_mav'] = data['Adj Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
# generates the signals based on the conditional statement
signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)
# creating the trading orders based on the positions column
signal_df['positions'] = signal_df['signal'].diff()
signal_df[signal_df['positions'] == -1.0]
# initialize the plot using plt
fig = plt.figure()
# Add a subplot and label for y-axis
plt1 = fig.add_subplot(111,  ylabel='Price in $')
data['Adj Close'].plot(ax=plt1, color='r', lw=2.)
# plot the short and long lookback moving averages
signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
# plotting the sell/buy signals
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, signal_df.short_mav[signal_df.positions == -1.0],'v', markersize=10, color='k')
plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, signal_df.short_mav[signal_df.positions == 1.0], '^', markersize=10, color='m')
plt.show()