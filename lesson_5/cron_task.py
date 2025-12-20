from celery import Celery
from datetime import datetime
import time

# Celery ilovasini yaratamiz (Redis broker sifatida)
app = Celery('cron_task', broker='redis://localhost:6379/0')

@app.task
def my_job():
    print(f"[{datetime.now()}] — Vazifa bajarildi ✅")

if __name__ == "__main__":
    # Worker’ni ishga tushirmasdan o'zimiz “cron” effektini beramiz
    print("⏳ Celery bilan avtomatik vazifa ishlayapti... Ctrl + C bilan to‘xtat.")
    while True:
        my_job.delay()  # Celery orqali backgroundda ishga yuboradi
        time.sleep(5)  # Har 5 soniyada ish bajaradi
