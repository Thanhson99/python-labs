import requests

def get_binance_order_book(symbol="BTCUSDT", depth=5):
    """Get top buy/sell orders from Binance"""
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={depth}"
    response = requests.get(url)
    data = response.json()
    
    bids = data.get("bids", [])  # Buy orders
    asks = data.get("asks", [])  # Sell orders

    return {
        "bids": bids,
        "asks": asks
    }
