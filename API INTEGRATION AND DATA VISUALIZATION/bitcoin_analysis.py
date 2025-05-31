import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Fetch Top 10 Cryptocurrencies from CoinCap
def fetch_top10_data():
    url = "https://rest.coincap.io/v3/assets?limit=08&&apiKey=b775409af48755ee25e431c1b4af14b7acf54f4a3bc18b6fc499c9982a33691e"
    response = requests.get(url)
    data = response.json()["data"]

    # Extract required fields
    names = [coin["name"] for coin in data]
    symbols = [coin["symbol"] for coin in data]
    prices = [float(coin["priceUsd"]) for coin in data]
    market_caps = [float(coin["marketCapUsd"]) for coin in data]

    df = pd.DataFrame({
        "Name": names,
        "Symbol": symbols,
        "Price (USD)": prices,
        "Market Cap (USD)": market_caps
    })

    return df

# Step 2: Visualize Bar and Pie Charts
def visualize_crypto_data(df):
    # Bar Chart for Price
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.bar(df["Symbol"], df["Price (USD)"], color='skyblue')
    plt.title("Top 10 Cryptos - Price in USD")
    plt.xlabel("Crypto Symbol")
    plt.ylabel("Price")
    plt.xticks(rotation=45)

    # Pie Chart for Market Cap Distribution
    plt.subplot(1, 2, 2)
    plt.pie(df["Market Cap (USD)"], labels=df["Symbol"], autopct='%1.1f%%', startangle=140)
    plt.title("Top 10 Cryptos - Market Cap Distribution")

    plt.tight_layout()
    plt.savefig("top10_crypto_visual.png")
    plt.show()

# Main
df = fetch_top10_data()
print("📊 Top 10 Cryptocurrencies:\n")
print(df[["Symbol", "Price (USD)", "Market Cap (USD)"]])
visualize_crypto_data(df)
