import requests
from src.tatum_endpoints import get_rest_url


def scan_recent_blocks_rest(address: str, scan_range: int, api_key: str, network: str):
    """
    Scan recent blocks using Tatum REST API.
    Returns:
        list of dicts with block info and matching transactions
        OR {"error": "..."} if REST is unavailable
    """

    rest_url = get_rest_url(network)
    headers = {"x-api-key": api_key}

    results = []

    # 1) Get current block height
    try:
        r = requests.get(f"{rest_url}/block/current", headers=headers, timeout=10)
        r.raise_for_status()
        current_height = r.json().get("height")
    except Exception as e:
        return {"error": f"REST unavailable: {e}"}

    # 2) Loop over recent blocks
    for height in range(current_height, current_height - scan_range, -1):
        try:
            # Get block hash
            r = requests.get(f"{rest_url}/block/{height}", headers=headers, timeout=10)
            r.raise_for_status()
            block_data = r.json()

            block_hash = block_data.get("hash")
            timestamp = block_data.get("time")

            # Get block transactions
            r = requests.get(f"{rest_url}/block/{block_hash}/txs", headers=headers, timeout=10)
            r.raise_for_status()
            txs = r.json()

            # Find matching transactions
            matching = []
            for tx in txs:
                if address in str(tx):
                    matching.append(tx)

            results.append({
                "height": height,
                "time": timestamp,
                "txs": matching
            })

        except Exception as e:
            return {"error": f"REST block scan failed at height {height}: {e}"}

    return results
