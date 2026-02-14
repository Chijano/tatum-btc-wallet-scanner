from src.wallet_scanner import scan_recent_blocks
from src.external_balance import get_address_balance


def analyze_wallet_activity(address: str):
    balance = get_address_balance(address)
    activities = []

    for block in scan_recent_blocks():
        block_height = block["height"]
        block_time = block["time"]

        for tx in block["txs"]:
            txid = tx["txid"]

            # RECEIVED
            for vout in tx.get("vout", []):
                spk = vout.get("scriptPubKey", {})
                if spk.get("address") == address:
                    activities.append({
                        "type": "RECEIVED",
                        "amount": vout["value"],
                        "txid": txid,
                        "block": block_height,
                        "time": block_time
                    })

            # SPENT
            for vin in tx.get("vin", []):
                prevout = vin.get("prevout", {})
                spk = prevout.get("scriptPubKey", {})
                if spk.get("address") == address:
                    activities.append({
                        "type": "SPENT",
                        "amount": prevout["value"],
                        "txid": txid,
                        "block": block_height,
                        "time": block_time
                    })

    if not activities:
        return (
            f"Address: {address}\n"
            f"Current balance: {balance} BTC\n"
            f"No on-chain activity detected in scanned range."
        )

    output = [
        f"Address: {address}",
        f"Current balance: {balance} BTC",
        "",
        "Activity detected:"
    ]

    for act in activities:
        output.append(
            f"\n[{act['type']}] {act['amount']} BTC\n"
            f"  Block: {act['block']}\n"
            f"  Time: {act['time']}\n"
            f"  TXID: {act['txid']}"
        )

    return "\n".join(output)
