# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2021-01-01', '2021-10-03')
moving_average = data['Adj Close'].rolling(window=20).mean()
# initializing the short and long lookback periods
short_lb = 10
mid_lb = 18
long_lb = 30
# initializing a new DataFrame called signal_df with a signal column
signal_df = pd.DataFrame(index=data.index)
signal_df['long_signal'] = 0.0
signal_df['mid_signal'] = 0.0
trade_revenue = 0
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
# calculating profits
def total_up(values_list):
    buy_value = np.sum(signal_df.actual_price[values_list == 1.0])
    sell_value = np.sum(signal_df.actual_price[values_list == -1.0])
    if len(signal_df.actual_price[values_list == -1.0]) != len(signal_df.actual_price[values_list == 1.0]):
        print("a trade is still running")
        sell_value += signal_df.actual_price[-1]
    total_value = (sell_value-buy_value)/buy_value*100/2
    return total_value

trade_revenue = total_up(signal_df.long_positions) + total_up(signal_df.mid_positions)
print(f"{round(trade_revenue, 2)}% revenue")
# initialize the plot using plt
fig = plt.figure()
# Add a subplot and label for y-axis
plt1 = fig.add_subplot(111,  ylabel='Price in $')
data['Adj Close'].plot(ax=plt1, color='r', lw=2.)
# plot the short and long lookback moving averages
signal_df[['short_mav', 'mid_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
# plotting the sell/buy signals
long_sell = signal_df.loc[signal_df.long_positions == -1.0].index
long_buy = signal_df.loc[signal_df.long_positions == 1.0].index
mid_sell = signal_df.loc[signal_df.mid_positions == -1.0].index
mid_buy = signal_df.loc[signal_df.mid_positions == 1.0].index

plt1.plot(long_buy, signal_df.actual_price[signal_df.long_positions == 1.0], '^', markersize=7, color='c')
plt1.plot(long_sell, signal_df.actual_price[signal_df.long_positions == -1.0], 'v', markersize=7, color='c')
plt1.plot(mid_buy, signal_df.actual_price[signal_df.mid_positions == 1.0], '^', markersize=7, color='m')
plt1.plot(mid_sell, signal_df.actual_price[signal_df.mid_positions == -1.0], 'v', markersize=7, color='m')
plt.show()
