MAINNET = "mainnet"
TESTNET = "testnet"


# Very simple, practical heuristics – enough for our use‑case
def detect_network(address: str) -> str:
    address = address.strip()

    # Bech32 mainnet: bc1...
    if address.startswith("bc1"):
        return MAINNET

    # Bech32 testnet: tb1...
    if address.startswith("tb1"):
        return TESTNET

    # Legacy / P2SH mainnet: 1..., 3...
    if address.startswith("1") or address.startswith("3"):
        return MAINNET

    # Legacy / P2SH testnet: m..., n..., 2...
    if address.startswith("m") or address.startswith("n") or address.startswith("2"):
        return TESTNET

    # Fallback – if unknown, default to mainnet
    return MAINNET
