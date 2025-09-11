"""
import time
import subprocess
import yaml
import os
from db_utils import get_engine
from sync_utils import sync_old_to_new
from score_pipeline import load_config, run_score_pipeline

def poll_pipeline(interval_sec=300):
    """Poll every 'interval_sec' seconds (default 5 minutes)."""
    config = load_config()
    engine = get_engine(config)
    print(f"Polling started... running every {interval_sec} seconds.")

    while True:
        print("\n--- Syncing old → new table ---")
        sync_old_to_new(engine, config)

        print("--- Triggering scoring pipeline ---")
        run_score_pipeline(engine, config)

        print(f"Sleeping for {interval_sec} seconds...\n")
        time.sleep(interval_sec)

if __name__ == "__main__":
    poll_pipeline(interval_sec=60)  # 1-min polling
"""

import time
import schedule
from db_utils import get_engine
from sync_utils import sync_old_to_new
from score_pipeline import load_config, run_score_pipeline

def job():
    config = load_config()
    engine = get_engine(config)
    
    print("\n--- Syncing old → new table ---")
    sync_old_to_new(engine, config)

    print("--- Triggering scoring pipeline ---")
    run_score_pipeline(engine, config)

def poll_pipeline():
    # Schedule the job every day at 12:00 PM
    schedule.every().day.at("12:00").do(job)

    print("Polling started... will run daily at 12:00 PM.")
    while True:
        schedule.run_pending()
        time.sleep(30)  # check every 30s

if __name__ == "__main__":
    poll_pipeline()
