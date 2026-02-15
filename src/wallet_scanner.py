import requests
import time

REST_URL = "https://bitcoin-testnet.gateway.tatum.io/rest"


def get_latest_height(api_key: str):
    headers = {"x-api-key": api_key}
    try:
        r = requests.get(f"{REST_URL}/block/current", headers=headers, timeout=10)
        r.raise_for_status()
        return r.json().get("height")
    except Exception:
        return None


def get_block_hash(height: int, api_key: str):
    headers = {"x-api-key": api_key}
    try:
        r = requests.get(f"{REST_URL}/block/hash/{height}", headers=headers, timeout=10)
        r.raise_for_status()
        return r.json().get("hash")
    except Exception:
        return None


def get_block(block_hash: str, api_key: str):
    headers = {"x-api-key": api_key}
    try:
        r = requests.get(f"{REST_URL}/block/{block_hash}.json", headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def scan_recent_blocks(scan_range: int, api_key: str):
    latest = get_latest_height(api_key)
    if latest is None:
        yield {"error": "rest_down"}
        return

    current_hash = get_block_hash(latest, api_key)
    if current_hash is None:
        yield {"error": "rest_down"}
        return

    for _ in range(scan_range):
        block = get_block(current_hash, api_key)
        if block is None:
            yield {"error": "rest_down"}
            return

        yield {
            "height": block["height"],
            "time": block["time"],
            "txs": block["tx"]
        }

        current_hash = block.get("previousblockhash")
        if not current_hash:
            break

        time.sleep(1)
