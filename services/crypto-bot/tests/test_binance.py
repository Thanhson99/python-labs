from modules.crypto.binance_service import get_binance_order_book

def test_binance_order_book():
    order_book = get_binance_order_book()
    bids = order_book["bids"]
    asks = order_book["asks"]
    
    assert isinstance(bids, list), "Bids must be a list"
    assert isinstance(asks, list), "Asks must be a list"
    assert len(bids) > 0, "Bids must not be empty"
    assert len(asks) > 0, "Asks must not be empty"

test_binance_order_book()
print("✅ Binance Order Book test passed!")
