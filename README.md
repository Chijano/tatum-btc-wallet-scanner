Tatum BTC Wallet Scanner
A lightweight Bitcoin wallet activity analyzer built in Python.
The tool scans recent blocks on Bitcoin mainnet or testnet and detects incoming transactions for a given address.
It uses Tatum’s RPC Gateway and includes a clean Tkinter GUI for easy use.

Features
- Incoming-only transaction detection
Pure vout-based heuristics for reliable incoming activity scanning.
- Automatic network detection
Supports Bech32 and legacy prefixes for both mainnet and testnet.
- RPC-based block scanning
Fetches recent blocks through Tatum’s RPC Gateway and inspects all transactions.
- Tkinter GUI
Simple, responsive interface with loading indicators and user-friendly error handling.
- Optimized for rate limits
Minimal API calls, retry logic, and graceful fallback behavior.

How It Works
- User enters a Bitcoin address.
- The app detects whether it belongs to mainnet or testnet.
- The scanner fetches recent blocks using Tatum’s RPC Gateway.
- Each transaction is inspected for outputs matching the target address.
- Incoming transactions are displayed in the GUI.

Requirements
The project uses only a few standard Python libraries plus:
- requests
- tkinter (included with Python)
- tkinter.scrolledtext
Install dependencies manually:
pip install requests

Installation
1) Clone the repository
git clone https://github.com/Chijano/tatum-btc-wallet-scanner.git
2) Enter the project directory
cd tatum-btc-wallet-scanner
3) Install dependencies
pip install requests

Running the App
python main.py

Project Structure
```
tatum-btc-wallet-scanner/
│
├── main.py
├── src/
│   ├── app.py
│   ├── block_scanner_rest.py
│   ├── block_scanner_rpc.py
│   ├── gui.py
│   ├── network_utils.py
│   └── tatum_endpoints.py
│
├── assets/
└── README.md
```

Notes
- This project focuses on incoming activity only.
- It does not check balances or use REST balance endpoints.
- Designed as a practical, interview-ready demonstration of API integration, GUI design, and blockchain analytics.
