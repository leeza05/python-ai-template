import requests

def get_top_coins(limit = 10):
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
    }

    response = requests.get(url, params=params, timeout=10)
    return response.json()


def display_coins(coins):
    print(f"\n{'Rank':<6}{'Name':<20}{'Symbol':<10}{'Price (USD)':<18}{'24h Change'}")
    print("-" * 65)
    
    for coin in coins:
        rank = coin["market_cap_rank"]
        name = coin["name"]
        symbol = coin["symbol"].upper()
        price = f"${coin['current_price']:,.2f}"
        change = coin["price_change_percentage_24h"]
        change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        
        print(f"{rank:<6}{name:<20}{symbol:<10}{price:<18}{change_str}")


if __name__ == "__main__":
    print("Fetching top 10 coin...")
    coins=get_top_coins(10)

    if(coins):
        display_coins(coins)
    else:
        print("No data fetched.")