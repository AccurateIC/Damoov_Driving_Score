
"""import yaml
from pathlib import Path
from score_pipeline import run_score_pipeline

if __name__ == "__main__":
    # Resolve base directory
    base_dir = Path(__file__).resolve().parent.parent.parent

    # Load config.yaml
    config_path = base_dir / "config.yaml"
    config = yaml.safe_load(open(config_path))

    # Path to SQLite database
    db_path = base_dir / config['database']['sqlite_path']

    print("🚀 Starting scoring pipeline regardless of new data...")

    # Run the scoring pipeline directly (no new data check)
    run_score_pipeline(str(db_path), config)

    print("✅ Scoring pipeline completed and SampleTable updated.")

"""

from pathlib import Path
import yaml
from score_pipeline import run_score_pipeline

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_path = base_dir / "config.yaml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    db_path = base_dir / config['database']['sqlite_path']
    print(f"📁 Using DB path: {db_path}")

    print("🚀 Starting scoring pipeline regardless of new data...")
    run_score_pipeline(str(db_path), config)
    print("✅ Scoring pipeline completed and SampleTable updated.")
