import os
import requests
from dotenv import load_dotenv

load_dotenv()
WHALE_ALERT_API_KEY = os.getenv("WHALE_ALERT_API_KEY")

def get_whale_alert_transactions():
    """Fetch whale transactions from Whale Alert"""
    url = f"https://api.whale-alert.io/v1/transactions?api_key={WHALE_ALERT_API_KEY}&min_value=1000000"
    response = requests.get(url).json()

    transactions = []
    if "transactions" in response:
        for tx in response["transactions"]:
            transactions.append({
                "symbol": tx["symbol"],
                "amount": tx["amount"],
                "from": tx["from"]["owner"],
                "to": tx["to"]["owner"]
            })
    
    return transactions
