import requests

def get_binance_order_book(symbol="BTCUSDT", depth=5):
    """Lấy 5 lệnh mua/bán lớn nhất từ Binance"""
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={depth}"
    response = requests.get(url)
    data = response.json()
    
    bids = data.get("bids", [])  # Lệnh mua
    asks = data.get("asks", [])  # Lệnh bán

    return {
        "bids": bids,
        "asks": asks
    }
