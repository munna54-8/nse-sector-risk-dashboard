import yfinance as yf
import pandas as pd
import os

SECTOR_TICKERS = {
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
    "Auto": ["MARUTI.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "HEROMOTOCO.NS"],
    "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "APOLLOHOSP.NS"],
    "FMCG": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "TATACONSUM.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS"],
}

all_tickers = [t for tickers in SECTOR_TICKERS.values() for t in tickers]
ticker_to_sector = {t: sector for sector, tickers in SECTOR_TICKERS.items() for t in tickers}

print(f"Fetching {len(all_tickers)} stocks across {len(SECTOR_TICKERS)} sectors...")
data = yf.download(all_tickers, period="1y", interval="1d", group_by="ticker")

os.makedirs("data/raw", exist_ok=True)
records = []

for ticker in all_tickers:
    try:
        close = data[ticker]["Close"].dropna()
        if len(close) < 50:
            print(f"  Skipping {ticker}: only {len(close)} trading days, too little data")
            continue
        for date, price in close.items():
            records.append({"ticker": ticker, "sector": ticker_to_sector[ticker], "date": date, "close": price})
        print(f"  {ticker}: {len(close)} days OK")
    except KeyError:
        print(f"  Skipping {ticker}: no data returned (delisted or wrong symbol)")

df = pd.DataFrame(records)
df.to_csv("data/raw/stock_prices.csv", index=False)
print(f"\nTotal price records collected: {len(df)}")
print(f"Stocks successfully collected: {df['ticker'].nunique()} of {len(all_tickers)}")