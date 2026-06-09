from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import pandas as pd
import requests
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME"))
BASE_URL = os.getenv("COINGECKO_BASE_URL")

def fetch_price_history(coin_id: str, days: int = 30):
    try:
        response = requests.get(
            f"{BASE_URL}/coins/{coin_id}/market_chart",
            params={
                "vs_currency": "usd",
                "days": days
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
        df = df[["date", "price"]]

        return df

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"CoinGecko error: {str(e)}")
    
def analyse_prices(df: pd.DataFrame):
    df = df.copy()
    
    df["7_day_avg"] = df["price"].rolling(window=7).mean()
    
    best_day = df.loc[df["price"].idxmax()]
    worst_day = df.loc[df["price"].idxmin()]
    
    overall_change = ((df["price"].iloc[-1] - df["price"].iloc[0]) / df["price"].iloc[0]) * 100
    
    return {
        "highest_price": {
            "date": str(best_day["date"]),
            "price": round(best_day["price"], 2)
        },
        "lowest_price": {
            "date": str(worst_day["date"]),
            "price": round(worst_day["price"], 2)
        },
        "overall_change_percent": round(overall_change, 2),
        "average_price": round(df["price"].mean(), 2),
        "latest_price": round(df["price"].iloc[-1], 2)
    }

@app.get("/analyse/{coin_id}")
def analyse_coin(coin_id: str, days: int = 30):
    df = fetch_price_history(coin_id, days)
    analysis = analyse_prices(df)
    
    return {
        "coin": coin_id,
        "days_analysed": days,
        "analysis": analysis
    }