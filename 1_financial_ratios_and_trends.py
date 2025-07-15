import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Hisse listesi
tickers = ["AKBNK.IS", "SISE.IS", "THYAO.IS", "BIMAS.IS", "ASELS.IS"]

# 2. Ticker nesneleri
companies = {t: yf.Ticker(t) for t in tickers}

data = []
for t, ticker in companies.items():
    info = ticker.info
    data.append({
        "Ticker": t,
        "Market_Cap": info.get("marketCap"),
        "Trailing_PE": info.get("trailingPE"),
        "Shares_Outstanding": info.get("sharesOutstanding"),
        "Book_Value": info.get("bookValue"),
    })

df = pd.DataFrame(data).dropna()
df["Equity"] = df["Book_Value"] * df["Shares_Outstanding"]
df["Equity_to_MCap"] = df["Equity"] / df["Market_Cap"]

print("🔹 Güncel Finansal Veriler:")
print(df[["Ticker", "Market_Cap", "Trailing_PE", "Equity_to_MCap"]])

# 4. Fiyat verisi
prices = yf.download(tickers, start="2024-07-01", end="2025-07-01")["Close"]
prices.plot(title="1 Yıllık Hisse Fiyat Trendi")
plt.ylabel("Fiyat (TL)")
plt.show()

# 5. Tahmini F/K analizi (aylık)
pe_trends = pd.DataFrame()
for ticker in tickers:
    hist = companies[ticker].history(period="1y", interval="1mo")
    equity = df.loc[df["Ticker"] == ticker, "Equity"].values[0]
    shares = df.loc[df["Ticker"] == ticker, "Shares_Outstanding"].values[0]
    eps = equity / shares
    pe_trends[ticker] = hist["Close"] / eps

pe_trends.plot(title="Tahmini F/K Trend Grafiği (Ay Bazında)")
plt.ylabel("F/K Tahmini")
plt.show()
