import pandas as pd
import requests
import json

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1
    }
    response = requests.get(url,params=params,timeout=10)
    data=response.json()

    df=pd.DataFrame(data)
    df = df[["market_cap_rank", "name", "symbol", "current_price", "price_change_percentage_24h", "market_cap", "total_volume"]]

    return df

def analyze_df(df):
    print("\n-----Top 10 Cryptocurrencies by Market Cap:-----")
    top_10 = df.sort_values("market_cap", ascending=False).head(10)
    print(top_10[[ "name", "current_price", "market_cap"]])

    print("\n-----Top gainers in the last 24 hours:-----")
    gainers = df[df["price_change_percentage_24h"]>0]
    print(gainers[["name", "price_change_percentage_24h"]])

    print("\n-----Top volume cryptocurrencies:-----")
    top_volume=df.sort_values("total_volume", ascending=False).head(5)
    print(top_volume[["name", "total_volume"]])

    print("\n-----Average price-----")
    avg_price=df["current_price"].mean()
    print(f"Average price: ${avg_price:.2f}")