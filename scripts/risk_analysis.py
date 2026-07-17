import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/stock_prices.csv", parse_dates=["date"])
df = df.sort_values(["ticker", "date"])

# Daily returns per stock
df["daily_return"] = df.groupby("ticker")["close"].pct_change()

# Per-stock stats: total return over the period, volatility (std of daily returns), annualized
stock_stats = df.groupby(["ticker", "sector"]).agg(
    start_price=("close", "first"),
    end_price=("close", "last"),
    daily_vol=("daily_return", "std"),
    trading_days=("close", "count")
).reset_index()

stock_stats["total_return_pct"] = ((stock_stats["end_price"] / stock_stats["start_price"]) - 1) * 100
stock_stats["annualized_vol_pct"] = stock_stats["daily_vol"] * np.sqrt(252) * 100

# Risk-adjusted return: how much return per unit of risk taken (simplified Sharpe-style ratio, no risk-free rate)
stock_stats["return_per_risk"] = stock_stats["total_return_pct"] / stock_stats["annualized_vol_pct"]

stock_stats = stock_stats.sort_values("return_per_risk", ascending=False)
stock_stats.to_csv("data/clean/stock_risk_stats.csv", index=False)

print("=== ALL 30 STOCKS, RANKED BY RETURN-PER-UNIT-OF-RISK ===")
print(stock_stats[["ticker", "sector", "total_return_pct", "annualized_vol_pct", "return_per_risk"]].round(2).to_string(index=False))

# Sector-level rollup
sector_stats = stock_stats.groupby("sector").agg(
    avg_return_pct=("total_return_pct", "mean"),
    avg_volatility_pct=("annualized_vol_pct", "mean"),
    avg_return_per_risk=("return_per_risk", "mean")
).round(2).sort_values("avg_return_per_risk", ascending=False)

sector_stats.to_csv("data/clean/sector_risk_stats.csv")
print("\n=== SECTOR-LEVEL SUMMARY, RANKED BY RISK-ADJUSTED RETURN ===")
print(sector_stats.to_string())

print("\n=== HIGHEST RAW RETURN (before adjusting for risk) ===")
print(stock_stats.sort_values("total_return_pct", ascending=False)[["ticker", "sector", "total_return_pct", "annualized_vol_pct"]].head(5).round(2).to_string(index=False))

print("\n=== HIGHEST VOLATILITY (riskiest individual stocks) ===")
print(stock_stats.sort_values("annualized_vol_pct", ascending=False)[["ticker", "sector", "total_return_pct", "annualized_vol_pct"]].head(5).round(2).to_string(index=False))