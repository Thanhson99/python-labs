from apscheduler.schedulers.background import BackgroundScheduler
from modules.news.news_fetcher import fetch_latest_news
from modules.news.summarizer import generate_summary
from bot.send_news import send_telegram_news
import os
import time

COIN_LIST_FILE = "data/coins_list.json"

def get_coin_list():
    """Read coin list from JSON file"""
    import json
    with open(COIN_LIST_FILE, "r") as f:
        data = json.load(f)
    return data.get("coins", [])

def job():
    """Scheduled job"""
    print("🔄 Fetching news...")
    coins = get_coin_list()  # Load coin list (e.g., ["BTC", "ETH"])
    
    news_list = fetch_latest_news(coins)  # Fetch news related to BTC and ETH
    if not news_list:
        print("❌ No new updates found!")
        return

    summary = generate_summary(news_list)  # Summarize content
    send_telegram_news(summary)  # Send summary to Telegram
