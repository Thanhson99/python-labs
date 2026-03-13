import os
import requests
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set your chat ID
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    """Send a Telegram message"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    response = send_telegram_message("🔥 Automated message send test!")
    print(response)
