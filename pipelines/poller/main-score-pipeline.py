# run_scores.py
from pathlib import Path
import yaml
from db_utils import get_engine

from score_pipeline import load_config, run_score_pipeline

if __name__ == "__main__":
    config = load_config()
    engine = get_engine(config)
    print(f"🚀 Starting scoring pipeline on {config['database']['type']} (table: {config['database']['main_table']})")
    run_score_pipeline(engine, config)
    print("🏁 Done.")
