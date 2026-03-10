from apscheduler.schedulers.background import BackgroundScheduler
from modules.news.news_fetcher import fetch_latest_news
from modules.news.summarizer import generate_summary
from bot.send_news import send_telegram_news
import os
import time

COIN_LIST_FILE = "data/coins_list.json"

def get_coin_list():
    """Đọc danh sách coin từ file JSON"""
    import json
    with open(COIN_LIST_FILE, "r") as f:
        data = json.load(f)
    return data.get("coins", [])

def job():
    """Job chạy định kỳ"""
    print("🔄 Fetching news...")
    coins = get_coin_list()  # Lấy danh sách coin (VD: ["BTC", "ETH"])
    
    news_list = fetch_latest_news(coins)  # Lấy tin tức có liên quan đến BTC & ETH
    if not news_list:
        print("❌ Không có tin mới!")
        return

    summary = generate_summary(news_list)  # Tổng hợp nội dung
    send_telegram_news(summary)  # Gửi bài viết lên Telegram
