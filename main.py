import time
from threading import Thread
import schedule

from app import app

from src.database import create_backup

def run_app():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

def schedule_backup():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    t = app.config.get("BACKUP_SCHEDULE_TIME", "00:00")
    schedule.every().day.at(t).do(create_backup)
    backup_process = Thread(target=schedule_backup, daemon=True)
    backup_process.start()
    run_app()
