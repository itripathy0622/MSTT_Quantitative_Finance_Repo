import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = "SPY"

data = yf.download(ticker, period="1y", interval="1d") # Download 1 month of daily data
data = data.dropna()

data["SMA20"] = data["Close"].rolling(window=20).mean() # Average of last 20 days
data["SMA50"] = data["Close"].rolling(window=50).mean() # Average of last 50 days

data["Signal"] = 0

data.loc[data["SMA20"] > data["SMA50"], "Signal"] = 1
data["Position"] = data["Signal"].diff()

data["Market_Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Market_Return"] * data["Signal"].shift(1)

data["Market_Cumulative"] = (1 + data["Market_Return"]).cumprod()
data["Strategy_Cumulative"] = (1 + data["Strategy_Return"]).cumprod()

print(data[["Close", "SMA20", "SMA50", "Signal", "Position", "Market_Cumulative", "Strategy_Cumulative"]].tail(10))

plt.figure(figsize=(10,5))

#plt.plot(data["Close"], label="Close Price")
#plt.plot(data["SMA20"], label="SMA20")
#plt.plot(data["SMA50"], label="SMA50")

plt.plot(data["Market_Cumulative"], label="Market Return")
plt.plot(data["Strategy_Cumulative"], label="Strategy Return")

plt.title("SMA Strategy vs Market")
plt.legend()
plt.show()

## If SMA20 > SMA50, Buy (1)
## IF SMA20 < SMA50, Sell (0)

