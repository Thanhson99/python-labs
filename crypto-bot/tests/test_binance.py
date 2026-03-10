from modules.crypto.binance_service import get_binance_order_book

def test_binance_order_book():
    bids, asks = get_binance_order_book()
    
    assert isinstance(bids, list), "Bids phải là danh sách"
    assert isinstance(asks, list), "Asks phải là danh sách"
    assert len(bids) > 0, "Bids không được rỗng"
    assert len(asks) > 0, "Asks không được rỗng"

test_binance_order_book()
print("✅ Binance Order Book test passed!")
