from datetime import datetime, timezone
from src.network_utils import detect_network
from src.block_scanner_rest import scan_recent_blocks_rest
from src.block_scanner_rpc import scan_recent_blocks_rpc


def simplify_transaction(tx):
    """Convert raw RPC transaction into a simple human-readable summary (incoming-only)."""

    txid = tx.get("txid", "unknown")

    recipients = []
    total_value = 0.0

    for vout in tx.get("vout", []):
        spk = vout.get("scriptPubKey", {})
        addr = spk.get("address")
        value = vout.get("value", 0.0)

        if addr:
            recipients.append((addr, value))
            total_value += value

    lines = [
        f"Transaction ID: {txid}",
        f"Total value moved: {total_value:.8f} BTC"
    ]

    if recipients:
        lines.append("To:")
        for addr, value in recipients:
            lines.append(f"  - {addr}: {value:.8f} BTC")

    return "\n".join(lines)


def analyze_wallet_activity(address: str, scan_range: int, api_key: str):
    """
    Main orchestrator for wallet analysis.
    1) Detect network
    2) Try REST scanner
    3) If REST fails → fallback to RPC
    4) Return formatted text for GUI
    """

    network = detect_network(address)

    # Try REST first
    rest_data = scan_recent_blocks_rest(address, scan_range, api_key, network)

    if isinstance(rest_data, dict) and "error" in rest_data:
        # REST failed → fallback to RPC
        rpc_data = scan_recent_blocks_rpc(address, scan_range, api_key, network)

        if isinstance(rpc_data, dict) and "error" in rpc_data:
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

    # Format output
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

        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        if txs:
            found_any = True
            output_lines.append(f"Activity found in block {height} at {dt}:")
            output_lines.append("")

            for tx in txs:
                simplified = simplify_transaction(tx)
                output_lines.append(simplified)
                output_lines.append("")

    if not found_any:
        output_lines.append("No activity found in the scanned blocks.")

    return "\n".join(output_lines)
