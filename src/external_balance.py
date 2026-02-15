import requests

REST_URL = "https://bitcoin-testnet.gateway.tatum.io/rest"
RPC_URL = "https://bitcoin-testnet.gateway.tatum.io"


def get_address_balance(address: str, api_key: str):
    """
    1) Try REST balance (new Tatum Gateway)
    2) If REST fails → fallback to RPC
    """

    headers = {"x-api-key": api_key}

    # --- REST FIRST ---
    try:
        r = requests.get(f"{REST_URL}/address/{address}", headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        funded = data.get("chain_stats", {}).get("funded_txo_sum", 0)
        spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
        sats = funded - spent
        return sats / 100_000_000

    except Exception:
        pass  # fallback to RPC

    # --- RPC FALLBACK ---
    payload = {
        "jsonrpc": "2.0",
        "id": "balance",
        "method": "getaddressbalance",
        "params": {"address": address}
    }

    r = requests.post(RPC_URL, json=payload, headers=headers, timeout=10)
    r.raise_for_status()

    sats = r.json().get("result", {}).get("balance", 0)
    return sats / 100_000_000
