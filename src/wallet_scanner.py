import time
from src.safe_request import safe_get

SCAN_RANGE = 1


def get_latest_height():
    url = "https://bitcoin-testnet.gateway.tatum.io/rest/block/current"
    r = safe_get(url)

    if "error" in r:
        return None

    return r["height"]


def get_block_hash(height: int):
    url = f"https://bitcoin-testnet.gateway.tatum.io/rest/block/hash/{height}"
    r = safe_get(url)

    if "error" in r:
        return None

    return r["hash"]


def get_block(block_hash: str):
    url = f"https://bitcoin-testnet.gateway.tatum.io/rest/block/{block_hash}.json"
    r = safe_get(url)

    if "error" in r:
        return None

    return r


def scan_recent_blocks():
    latest_height = get_latest_height()
    if latest_height is None:
        yield {"error": "tatum_unavailable"}
        return

    current_hash = get_block_hash(latest_height)
    if current_hash is None:
        yield {"error": "tatum_unavailable"}
        return

    for _ in range(SCAN_RANGE):
        block = get_block(current_hash)
        if block is None:
            yield {"error": "tatum_unavailable"}
            return

        yield {
            "height": block["height"],
            "time": block["time"],
            "txs": block["tx"]
        }

        time.sleep(3)

        current_hash = block.get("previousblockhash")
        if not current_hash:
            break
