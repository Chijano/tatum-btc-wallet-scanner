import requests


def get_btc_price_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        raise Exception(f"Failed to fetch BTC price: {r.status_code}")

    data = r.json()
    return data["bitcoin"]["usd"]
