from src.safe_request import safe_get

BASE_URL = "https://bitcoin-testnet.gateway.tatum.io/rest"
SCAN_RANGE = 3


def get_latest_height():
    url = f"{BASE_URL}/chaininfo.json"
    r = safe_get(url)
    return r.json()["blocks"]


def get_block_hash(height: int):
    url = f"{BASE_URL}/blockhashbyheight/{height}.json"
    r = safe_get(url)
    return r.json()["blockhash"]


def get_block(block_hash: str):
    url = f"{BASE_URL}/block/{block_hash}.json"
    r = safe_get(url)
    return r.json()


def scan_recent_blocks():
    latest_height = get_latest_height()
    current_hash = get_block_hash(latest_height)

    for _ in range(SCAN_RANGE):
        block = get_block(current_hash)

        yield {
            "height": block["height"],
            "time": block["time"],
            "txs": block["tx"]
        }

        current_hash = block.get("previousblockhash")
        if not current_hash:
            break
