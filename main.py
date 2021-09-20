# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2020-09-01', '2021-09-01')
# Calculating returns
mdata = data.resample('M').apply(lambda x: x[-1])
monthly_return = mdata['Adj Close'].pct_change()
# Plot graph of monthly prices
mdata['Adj Close'].plot()
plt.show()
# Plot graph of simple moving average
moving_average = data['Adj Close'].rolling(window=35).mean()
moving_average.plot()
plt.show()