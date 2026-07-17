# NSE Sector Rotation & Risk-Adjusted Return Dashboard

## Problem
Which Indian stock market sectors are actually delivering returns worth the risk taken — not just which ones moved the most? This project compares 30 NSE-listed stocks across 6 sectors using risk-adjusted return, not raw price performance alone.

## Data source & collection method
One year of daily closing prices for 30 NSE-listed stocks across Banking, IT, Auto, Pharma, FMCG, and Energy, pulled directly via the `yfinance` library — no API key or signup required. 7,488 total price records.

## Approach
- Python (yfinance, Pandas, NumPy) to pull and process price history
- Calculated daily returns, then annualized volatility (standard deviation of daily returns × √252 trading days) per stock
- Built a simplified Sharpe-style ratio (total return ÷ annualized volatility) to rank stocks and sectors by return earned per unit of risk taken, not just raw performance

## Key findings
- **IT was the only sector with both a negative average return (-20.4%) and the highest average volatility (27.2%) of any sector** — every single IT stock in the basket underperformed on a risk-adjusted basis
- **Auto delivered the best risk-adjusted return (+0.71)**, driven by Eicher Motors (+35.5%) and Bajaj Auto (+27.0%) — high volatility that was actually compensated for by strong returns
- **ITC posted the worst raw return (-30.7%) while carrying one of the lowest volatilities in the dataset** — a poor outcome that isn't explainable as "high risk, high reward gone wrong"
- Reliance, India's largest company by market cap, posted a negative return (-9.7%) over the period

## Limitations
This is an educational analysis of one specific 1-year window, not investment advice. The risk-adjusted metric used is simplified (no risk-free rate subtracted) and intended for relative comparison within this dataset only.

## Tools
Python, yfinance, Pandas, NumPy, Chart.js

## Dashboard
[paste your GitHub Pages link here once live]