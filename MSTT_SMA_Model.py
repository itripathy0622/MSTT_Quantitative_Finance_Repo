import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sets cache location
yf.set_tz_cache_location(".custom/cache/location")


Ticker = "TSLA"

# ------ Downloading data ---------
# data = yf.download(ticker, begin="", end="")
data = yf.download(Ticker, period = "1y", interval = "1d")

data = data.dropna()

print(data.head())

# -------- SMA Logic ---------

# Create new column of 20 day mean; Rolling means using last 20 days
data["SMA20"] = data["Close"].rolling(window = 20).mean()

data["SMA50"] = data["Close"].rolling(window = 50).mean()


# --------- Plotting Close and SMA ----------

# plt.figure(figsize=(10,5))
# plt.plot(data["Close"], label = ["Close Price"])
# plt.plot(data["SMA20"], label="SMA20")
# plt.plot(data["SMA50"], label="SMA50")
# plt.title("SMA20 vs SMA50 vs Close")
# plt.legend()
# plt.show()


# 1 is a hold, 0 is a sell
data.loc[data["SMA20"] > data["SMA50"], "Signal"] = 1
data["Market_Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Market_Return"] * data["Signal"].shift(1)

# What market did
data["Market_Cumulative"] = (1 + data["Market_Return"]).cumprod()

# Cumulative
data["Strategy_Cumulative"] = (1 + data["Strategy_Return"]).cumprod()

# ----- Plotting Market vs Strategy Cumulative Returns -----
plt.figure()
# plt.plot(data["Close"], label = "Close Price")
plt.plot(data["Market_Cumulative"], label = "Market_Cumulative")
plt.plot(data["Strategy_Cumulative"], label = "Strategy_Return")
plt.title("Market vs Strategy Return")
plt.legend()
plt.show()