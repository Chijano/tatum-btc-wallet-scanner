from src.network_utils import MAINNET, TESTNET


# REST endpoints
REST_ENDPOINTS = {
    MAINNET: "https://bitcoin-mainnet.gateway.tatum.io/rest",
    TESTNET: "https://bitcoin-testnet.gateway.tatum.io/rest",
}

# RPC endpoints
RPC_ENDPOINTS = {
    MAINNET: "https://bitcoin-mainnet.gateway.tatum.io",
    TESTNET: "https://bitcoin-testnet.gateway.tatum.io",
}


def get_rest_url(network: str) -> str:
    """Return REST base URL for mainnet/testnet."""
    return REST_ENDPOINTS.get(network, REST_ENDPOINTS[MAINNET])


def get_rpc_url(network: str) -> str:
    """Return RPC base URL for mainnet/testnet."""
    return RPC_ENDPOINTS.get(network, RPC_ENDPOINTS[MAINNET])
