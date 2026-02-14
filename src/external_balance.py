import requests


def get_address_balance(address: str) -> float:
    url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data["final_balance"] / 1e8
