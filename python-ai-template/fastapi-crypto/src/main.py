from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME"))
BASE_URL = os.getenv("COINGECKO_BASE_URL")

class CoinSummary(BaseModel):
    rank:int
    name:str
    symbol:str
    price:float
    change_24h:float

@app.get("/")
def root():
    return {"app":os.getenv("APP_NAME"), "status":"running"}


@app.get("/coins", response_model=list[CoinSummary])
def get_top_coins(limit: int = 10):
    try:
        response = requests.get(
            f"{BASE_URL}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": limit,
                "page": 1
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return [
            CoinSummary(
                rank=coin["market_cap_rank"],
                name=coin["name"],
                symbol=coin["symbol"].upper(),
                price=coin["current_price"],
                change_24h=coin["price_change_percentage_24h"]
            )
            for coin in data
        ]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"CoinGecko error: {str(e)}")
    
    
@app.get("/coins/{coin_id}")
def get_coin(coin_id: str):
    try:
        response = requests.get(
            f"{BASE_URL}/coins/{coin_id}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {
            "name": data["name"],
            "symbol": data["symbol"].upper(),
            "price": data["market_data"]["current_price"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
            "all_time_high": data["market_data"]["ath"]["usd"]
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"CoinGecko error: {str(e)}")