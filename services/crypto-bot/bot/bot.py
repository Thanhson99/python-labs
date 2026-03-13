import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token from .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command to verify bot health"""
    await update.message.reply_text("🔥 Bot connected successfully! Type /test to receive a message.")

async def test_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test command to send a sample message"""
    await update.message.reply_text("✅ Bot is working correctly!")

def main():
    """Start Telegram bot"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
