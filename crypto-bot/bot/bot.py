import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token từ .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Thiết lập logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh /start để kiểm tra bot hoạt động"""
    await update.message.reply_text("🔥 Bot đã kết nối thành công! Gõ /test để nhận tin nhắn.")

async def test_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh /test để gửi tin nhắn mẫu"""
    await update.message.reply_text("✅ Bot đang hoạt động tốt!")

def main():
    """Khởi động bot Telegram"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_message))

    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
