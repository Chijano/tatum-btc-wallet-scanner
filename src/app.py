from src.wallet_scanner import scan_recent_blocks
from src.external_balance import get_address_balance


def analyze_wallet_activity(address: str, scan_range: int, api_key: str):
    results = []
    rest_down = False
    found_activity = False

    # Block scan (REST only)
    for block in scan_recent_blocks(scan_range, api_key):
        if "error" in block:
            rest_down = True
            break

        height = block["height"]
        timestamp = block["time"]

        for tx in block["txs"]:
            if address in str(tx):
                found_activity = True
                results.append(f"Activity in block {height} at time {timestamp}")
                results.append(str(tx))

    # Balance (REST → RPC fallback)
    balance_btc = get_address_balance(address, api_key)
    results.append(f"Balance: {balance_btc} BTC")

    if rest_down:
        results.insert(0, "REST API unavailable. Block scan skipped.")

    if not found_activity:
        results.insert(1, "No activity found in scanned blocks.")

    return "\n".join(results)
