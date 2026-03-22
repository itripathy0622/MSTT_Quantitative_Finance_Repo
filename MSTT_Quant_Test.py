import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = "SPY"

data = yf.download(ticker, period="1y", interval="1d") # Download 1 month of daily data
data.columns = data.columns.get_level_values(0)
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

data["Close"] = data["Close"].squeeze()

data["Entry"] = (data["Close"] > data["SMA20"]) & (data["Close"].shift(1) <= data["SMA20"].shift(1))
data["Exit"] = (data["Close"] < data["SMA20"]) & (data["Close"].shift(1) >= data["SMA20"].shift(1))

data["Buy_Signal"] = data["Close"].where(data["Entry"])
data["Sell_Signal"] = data["Close"].where(data["Exit"])

initial_cash = 10000
cash = initial_cash
shares = 0

portfolio_values = []

for i in range(len(data)):
    price = data["Close"].iloc[i]

    # BUY (only use 50% of cash)
    if data["Entry"].iloc[i] and cash > 0:
        invest_amount = cash * 0.5
        shares += invest_amount / price
        cash -= invest_amount

    # SELL (sell 50% of shares)
    elif data["Exit"].iloc[i] and shares > 0:
        sell_amount = shares * 0.5
        cash += sell_amount * price
        shares -= sell_amount

    portfolio_value = cash + shares * price
    portfolio_values.append(portfolio_value)

data["Portfolio_Fractional"] = portfolio_values

data["Market_Return"] = data["Close"] / data["Close"].iloc[0] * 10000

print(data["Entry"].sum())
print(data["Exit"].sum())


### Plotting and Graphing Information ###
#plt.figure(figsize=(10,5))

#plt.plot(data["Close"], label="Close Price")
#plt.plot(data["SMA20"], label="SMA20")
#plt.plot(data["SMA50"], label="SMA50")

#plt.plot(data["Market_Cumulative"], label="Market Return")
#plt.plot(data["Strategy_Cumulative"], label="Strategy Return")

plt.figure(figsize=(12,6))

# Price + SMA
plt.plot(data["Close"], label="Close Price", alpha=0.7)
plt.plot(data["SMA20"], label="SMA20", linestyle="--")
plt.plot(data["SMA50"], label="SMA50", linestyle="--")

# BUY markers
plt.scatter(data.index, data["Buy_Signal"], 
            label="Buy", marker="^", color="green", s=100)

# SELL markers
plt.scatter(data.index, data["Sell_Signal"], 
            label="Sell", marker="v", color="red", s=100)

plt.title("SMA Strategy Signals")
plt.legend()
plt.show()

## If SMA20 > SMA50, Buy (1)
## IF SMA20 < SMA50, Sell (0)

