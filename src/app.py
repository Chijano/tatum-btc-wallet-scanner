from src.wallet_scanner import scan_recent_blocks
from src.external_balance import get_address_balance
from src.price_fetcher import get_btc_price_usd


def analyze_wallet_activity(address: str):
    balance = get_address_balance(address)
    btc_price = get_btc_price_usd()
    usd_value = balance * btc_price

    activities = []
    rest_available = True

    for block in scan_recent_blocks():

        if "error" in block:
            rest_available = False
            break

        block_height = block["height"]
        block_time = block["time"]

        for tx in block["txs"]:
            txid = tx["txid"]

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

    output = [
        f"Address: {address}",
        f"Current balance: {balance} BTC",
        f"Current BTC price: {btc_price} USD",
        f"Wallet value: {usd_value:.2f} USD",
        ""
    ]

    if not rest_available:
        output.append("Blockchain activity: REST API unavailable.")
        return "\n".join(output)

    if not activities:
        output.append("No on-chain activity detected in scanned range.")
        return "\n".join(output)

    output.append("Activity detected:")
    for act in activities:
        output.append(
            f"\n[{act['type']}] {act['amount']} BTC\n"
            f"  Block: {act['block']}\n"
            f"  Time: {act['time']}\n"
            f"  TXID: {act['txid']}"
        )

    return "\n".join(output)