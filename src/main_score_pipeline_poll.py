
from score_pipeline import run_score_pipeline
import yaml
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    # Get root path (assuming this file is in src/)
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config.yaml"

    # Load config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Resolve db_path relative to project root
    db_path = base_dir / config['database']['sqlite_path']
    run_score_pipeline(str(db_path), config)

if __name__ == "__main__":

    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=1)  # ⏱ Run every 3 hours
    print("Polling started. Checking for new data every 1 minute...")
    scheduler.start()