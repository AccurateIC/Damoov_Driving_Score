
import time
import subprocess
import yaml
import os

def load_config():
    """Load DB/config details from config.yaml at project root."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_main_pipeline():
    """Run your existing main_score_pipeline.py as a subprocess."""
    try:
        subprocess.run(
            ["python", "src/app/main-score-pipeline.py"],
            check=True
        )
        print("Pipeline executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running pipeline: {e}")

def poll_pipeline(interval_sec=300):
    """Poll every 'interval_sec' seconds (default 5 minutes)."""
    config = load_config()  # not used directly but validates config.yaml exists
    print(f"Polling started... running every {interval_sec} seconds.")
    
    while True:
        print("\n--- Triggering pipeline ---")
        run_main_pipeline()
        print(f"Sleeping for {interval_sec} seconds...\n")
        time.sleep(interval_sec)

if __name__ == "__main__":
    poll_pipeline(interval_sec=60)  # change to 60 if you want 1-min polling
