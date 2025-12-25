import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. Hisse listesi
tickers = ["AKBNK.IS", "SISE.IS", "THYAO.IS", "BIMAS.IS", "ASELS.IS"]

# 2. Ticker nesneleri
companies = {t: yf.Ticker(t) for t in tickers}

# 3. Finansal oranlar
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

# Equity / Market Cap oranı
df["Equity"] = df["Book_Value"] * df["Shares_Outstanding"]
df["Equity_to_MCap"] = df["Equity"] / df["Market_Cap"]

print("🔹 Finansal Oran Karşılaştırması")
print(df[["Ticker", "Trailing_PE", "Equity_to_MCap"]])

# =========================
# GRAFİKLER
# =========================

# Trailing P/E karşılaştırması
plt.bar(df["Ticker"], df["Trailing_PE"])
plt.title("Trailing P/E Karşılaştırması")
plt.ylabel("F/K Oranı")
plt.tight_layout()
plt.show()

# Equity / Market Cap karşılaştırması
plt.bar(df["Ticker"], df["Equity_to_MCap"])
plt.title("Equity / Market Cap Oranı")
plt.ylabel("Oran")
plt.tight_layout()
plt.show()

# =========================
# FİYAT TRENDİ
# =========================

prices = yf.download(tickers, start="2024-07-01", end="2025-07-01")["Close"]
prices.plot(title="1 Yıllık Hisse Fiyat Trendi")
plt.ylabel("Fiyat (TL)")
plt.tight_layout()
plt.show()
