import requests
from src.tatum_endpoints import get_rpc_url


def rpc_call(url: str, api_key: str, method: str, params=None):
    """Generic JSON-RPC call helper."""
    headers = {"x-api-key": api_key}
    payload = {
        "jsonrpc": "2.0",
        "id": method,
        "method": method,
        "params": params or []
    }

    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    if "error" in data:
        raise Exception(data["error"].get("message"))

    return data.get("result")


def scan_recent_blocks_rpc(address: str, scan_range: int, api_key: str, network: str):
    """
    Scan recent blocks using Tatum RPC API.
    Returns:
        list of dicts with block info and matching transactions
        OR {"error": "..."} if RPC is unavailable
    """

    rpc_url = get_rpc_url(network)

    try:
        # 1) Get current block height
        current_height = rpc_call(rpc_url, api_key, "getblockcount")
    except Exception as e:
        return {"error": f"RPC unavailable: {e}"}

    results = []

    # 2) Loop over recent blocks
    for height in range(current_height, current_height - scan_range, -1):
        try:
            # Get block hash
            block_hash = rpc_call(rpc_url, api_key, "getblockhash", [height])

            # Get full block (verbosity 2 = decoded)
            block = rpc_call(rpc_url, api_key, "getblock", [block_hash, 2])

            timestamp = block.get("time")
            txs = block.get("tx", [])

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
            return {"error": f"RPC block scan failed at height {height}: {e}"}

    return results
