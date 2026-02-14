from src.app import analyze_wallet_activity

if __name__ == "__main__":
    address = input("Enter testnet address: ").strip()
    print(analyze_wallet_activity(address))
