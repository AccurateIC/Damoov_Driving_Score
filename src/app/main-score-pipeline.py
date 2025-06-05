
import yaml
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from score_pipeline import run_score_pipeline
import sqlite3

last_uid_path = Path(".last_uid")

def get_latest_unique_id(db_path):
    with sqlite3.connect(db_path) as conn:
        result = conn.execute("SELECT MAX(unique_id) FROM SampleTable").fetchone()
        return result[0] if result else None

def job():
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_path = base_dir / "config.yaml"
    config = yaml.safe_load(open(config_path))

    db_path = base_dir / config['database']['sqlite_path']
    latest_uid = get_latest_unique_id(str(db_path))

    last_uid = None
    if last_uid_path.exists():
        last_uid = last_uid_path.read_text().strip()

    if str(latest_uid) != last_uid:
        print(f"🟢 New data detected (last_uid: {last_uid} → latest_uid: {latest_uid})")
        run_score_pipeline(str(db_path), config)
        last_uid_path.write_text(str(latest_uid))
    else:
        print("⏳ No new data found. Skipping scoring.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=10)  # or hours=3
    print("🚀 Polling started. Will run only if new data is found.")
    scheduler.start()
