# Crypto Telegram Bot 🚀

## 1. Cài Đặt

```sh
git clone https://github.com/your-repo/crypto-bot.git
cd crypto-bot
pip install -r requirements.txt
cp .env.example .env  # Cập nhật API token vào file .env


crypto-bot/
│── bot/                     # Chứa bot Telegram
│   ├── commands/            # Chứa các lệnh của bot
│   │   ├── start.py
│   │   ├── news.py
│   │   ├── price.py
│   │   ├── whale.py
│   ├── handlers/            # Chứa các trình xử lý sự kiện
│   │   ├── message_handler.py
│   │   ├── callback_handler.py
│   ├── bot.py               # File chính khởi động bot
│   ├── config.py            # Load config từ .env
│   ├── scheduler.py         # Chạy bot theo lịch
│   ├── send_message.py      # File gửi tin nhắn test
│   ├── send_news.py         # File gửi tin tức tổng hợp
│
├── core/                    # Chứa các thư viện lõi, tiện ích
│   ├── logger.py            # Xử lý logging
│   ├── utils.py             # Các hàm tiện ích
│
├── data/                    # Chứa dữ liệu tĩnh
│   ├── alerts.json
│   ├── coins_list.json
│   ├── sources.json         # Danh sách nguồn tin tức
│
├── logs/                    # Chứa file log
│   ├── bot.log
│
├── modules/                 # Chứa các service riêng biệt
│   ├── crypto/              # Các module liên quan đến crypto
│   │   ├── binance_service.py
│   │   ├── etherscan_service.py
│   │   ├── glassnode_service.py
│   │   ├── price_tracker.py
│   ├── news/                # Module về tin tức
│   │   ├── news_fetcher.py
│   │   ├── rss_fetcher.py
│   │   ├── scraper.py
│   │   ├── summarizer.py
│   │   ├── deduplicator.py
│   ├── whale/               # Module về cá voi
│   │   ├── whale_alert.py
│   │   ├── whale_alert_service.py
│
├── tests/                   # Chứa các test case
│   ├── test_binance.py
│   ├── test_bot.py
│   ├── test_whale_tracker.py
│
├── .env                     # Chứa các biến môi trường
├── main.py                  # File chạy chính
├── README.md                # Hướng dẫn sử dụng
├── requirements.txt         # Danh sách thư viện cần cài đặt
├── run.sh                   # Script chạy bot
