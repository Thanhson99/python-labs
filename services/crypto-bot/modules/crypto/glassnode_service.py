import os
import requests
from dotenv import load_dotenv

load_dotenv()
GLASSNODE_API_KEY = os.getenv("GLASSNODE_API_KEY")

def get_glassnode_data(coin_list):
    """Lấy dữ liệu cá voi từ Glassnode"""
    transactions = []
    
    for coin in coin_list:
        url = f"https://api.glassnode.com/v1/metrics/addresses/supply_distribution?api_key={GLASSNODE_API_KEY}&a={coin}&s=1704067200"
        response = requests.get(url).json()

        if response:
            whale_data = response[-1]  # Lấy dữ liệu mới nhất
            transactions.append({
                "symbol": coin,
                "amount": whale_data["balance"],
                "from": "Whale Wallet",
                "to": "Holding"
            })

    return transactions
