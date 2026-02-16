from datetime import datetime, timezone
from src.network_utils import detect_network
from src.block_scanner_rest import scan_recent_blocks_rest
from src.block_scanner_rpc import scan_recent_blocks_rpc


def simplify_transaction(tx, target_address):
    """Convert raw RPC transaction into a simple human-readable summary."""

    txid = tx.get("txid", "unknown")

    # Extract senders (vin)
    senders = []
    for vin in tx.get("vin", []):
        if "txid" in vin:
            senders.append(vin["txid"])

    # Extract recipients (vout)
    recipients = []
    total_value = 0.0
    incoming = False
    outgoing = False

    for vout in tx.get("vout", []):
        addr = vout.get("scriptPubKey", {}).get("address")
        value = vout.get("value", 0.0)

        if addr:
            recipients.append((addr, value))
            total_value += value

            if addr == target_address:
                incoming = True

    # Determine direction
    direction = "INCOMING" if incoming else "OUTGOING" if outgoing else "UNKNOWN"

    # Build readable text
    lines = [
        f"Transaction ID: {txid}",
        f"Direction: {direction}",
        f"Total value moved: {total_value:.8f} BTC"
    ]

    if senders:
        lines.append("From:")
        for s in senders:
            lines.append(f"  - {s}")

    if recipients:
        lines.append("To:")
        for addr, value in recipients:
            lines.append(f"  - {addr}: {value:.8f} BTC")

    return "\n".join(lines)


def analyze_wallet_activity(address: str, scan_range: int, api_key: str):
    """
    Main orchestrator for wallet analysis.
    1) Detect network (mainnet/testnet)
    2) Try REST scanner
    3) If REST fails → fallback to RPC
    4) Return formatted text for GUI
    """

    network = detect_network(address)

    # --- Try REST first ---
    rest_data = scan_recent_blocks_rest(address, scan_range, api_key, network)

    if isinstance(rest_data, dict) and "error" in rest_data:
        # REST failed → fallback to RPC
        rpc_data = scan_recent_blocks_rpc(address, scan_range, api_key, network)

        if isinstance(rpc_data, dict) and "error" in rpc_data:
            # Both failed → return error
            return (
                "Both REST and RPC scanning failed.\n"
                f"REST error: {rest_data['error']}\n"
                f"RPC error: {rpc_data['error']}"
            )

        scan_results = rpc_data
        method_label = "RPC"

    else:
        scan_results = rest_data
        method_label = "REST"

    # --- Format output ---
    output_lines = [
        f"Network detected: {network.upper()}",
        f"Scanning method used: {method_label}",
        ""
    ]

    found_any = False

    for block in scan_results:
        height = block["height"]
        timestamp = block["time"]
        txs = block["txs"]

        # Modern timezone-aware timestamp
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        if txs:
            found_any = True
            output_lines.append(f"Activity found in block {height} at {dt}:")
            output_lines.append("")

            for tx in txs:
                simplified = simplify_transaction(tx, address)
                output_lines.append(simplified)
                output_lines.append("")

    if not found_any:
        output_lines.append("No activity found in the scanned blocks.")

    return "\n".join(output_lines)
