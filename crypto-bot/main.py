from bot.scheduler import job
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULE_INTERVAL = int(os.getenv("SCHEDULE_INTERVAL", 6))  # Mặc định chạy mỗi 6 giờ

if __name__ == "__main__":
    print(f"✅ Bot đang chạy, sẽ cập nhật tin tức mỗi {SCHEDULE_INTERVAL} giờ...")

    # 🚀 Chạy ngay lần đầu tiên khi bot khởi động
    job()  

    # Khởi tạo scheduler để chạy lặp lại
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", hours=SCHEDULE_INTERVAL)
    scheduler.start()

    try:
        while True:
            time.sleep(1)  # Giữ chương trình chạy
    except KeyboardInterrupt:
        print("❌ Dừng bot")
        scheduler.shutdown()
