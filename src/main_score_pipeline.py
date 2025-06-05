
from score_pipeline import run_score_pipeline
import yaml
from pathlib import Path

if __name__ == "__main__":
    # Get root path (assuming this file is in src/)
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config.yaml"

    # Load config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Resolve db_path relative to project root
    db_path = base_dir / config['database']['sqlite_path']

    # Run pipeline
    run_score_pipeline(str(db_path), config)
