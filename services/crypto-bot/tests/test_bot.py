import pytest
from bot.send_message import send_telegram_message

def test_send_telegram_message():
    """Test Telegram message sending"""
    response = send_telegram_message("🔍 Test message from pytest!")
    
    assert response["ok"] is True
    assert response["result"]["chat"]["id"] is not None
    assert response["result"]["text"] == "🔍 Test message from pytest!"
