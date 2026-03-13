import os
import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_etherscan_whale_transactions(coin_list):
    """Fetch whale transaction data from Etherscan"""
    transactions = []
    for coin, contract_address in coin_list.items():
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()

        if response["status"] == "1":  # Has data
            for tx in response["result"]:
                if int(tx["value"]) > 10**18:  # Keep only transactions larger than 1 ETH
                    transactions.append({
                        "symbol": coin,
                        "amount": int(tx["value"]) / 10**18,
                        "from": tx["from"],
                        "to": tx["to"]
                    })
    return transactions
