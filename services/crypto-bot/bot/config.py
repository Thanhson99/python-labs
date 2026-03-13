import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

WHITELISTED_USERS = [123456789, 987654321]  # Allowed Telegram user IDs
