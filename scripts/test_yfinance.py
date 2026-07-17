import yfinance as yf

# NSE tickers need a ".NS" suffix
tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "TATAMOTORS.NS"]

data = yf.download(tickers, period="6mo", interval="1d", group_by="ticker")

print("Shape of data:", data.shape)
print("\nColumns available:", data.columns.tolist()[:10])

for t in tickers:
    close_prices = data[t]["Close"].dropna()
    print(f"\n{t}: {len(close_prices)} trading days, latest close: {close_prices.iloc[-1]:.2f}")