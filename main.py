# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2020-09-21', '2021-09-21')
# Calculating returns
mdata = data.resample('M').apply(lambda x: x[-1])
monthly_return = mdata['Adj Close'].pct_change()
# Plot graph of monthly prices
data['Adj Close'].plot()
plt.show()
# Plot graph of simple moving average
moving_average = data['Adj Close'].rolling(window=20).mean()
moving_average.plot()
plt.show()