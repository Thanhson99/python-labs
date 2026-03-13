from bot.scheduler import job
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULE_INTERVAL = int(os.getenv("SCHEDULE_INTERVAL", 6))  # Default interval runs every 6 hours

if __name__ == "__main__":
    print(f"✅ Bot is running, news will refresh every {SCHEDULE_INTERVAL} hours...")

    # 🚀 Run once immediately at startup
    job()  

    # Initialize scheduler for recurring execution
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", hours=SCHEDULE_INTERVAL)
    scheduler.start()

    try:
        while True:
            time.sleep(1)  # Keep process alive
    except KeyboardInterrupt:
        print("❌ Stopping bot")
        scheduler.shutdown()
