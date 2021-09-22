# importing required packages
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Getting the data by specifying the stock ticker, start date, and end date
data = yf.download('^SP500TR', '2020-09-01', '2021-09-01')
moving_average = data['Adj Close'].rolling(window=20).mean()
# initializing the short and long lookback periods
short_lb = 50
long_lb = 120
# initializing a new DataFrame called signal_df with a signal column
signal_df = pd.DataFrame(index=data.index)signal_df['signal'] = 0.0