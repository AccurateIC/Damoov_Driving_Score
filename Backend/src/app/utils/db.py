"""import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

_engine = None
CONFIG = {}

# Load config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(BASE_DIR)
CONFIG_PATH = os.path.join(SRC_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f) or {}

db_cfg = CONFIG.get("database", {})

def setup_database():
    
    global _engine
    if _engine is None:  # only create once
        if db_cfg.get("type", "sqlite").lower() == "mysql":
            _engine = create_engine(
                f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['name']}",
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,
                future=True,
            )
        else:
            _engine = create_engine(
                f"sqlite:///{db_cfg['sqlite_path']}",
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                future=True,
            )
    return _engine
"""

import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

_engine = None
CONFIG = {}

# Load config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(BASE_DIR)
CONFIG_PATH = os.path.join(SRC_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f) or {}

db_cfg = CONFIG.get("database", {})

def setup_database():
    """Initialize a global SQLAlchemy engine (MySQL or SQLite)."""
    global _engine
    if _engine is None:  # only create once
        if db_cfg.get("type", "sqlite").lower() == "mysql":
            _engine = create_engine(
                f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['name']}",
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_recycle=1800,   # recycle every 30 min (safer than 1 hr)
                pool_pre_ping=True, # test connections before use
                future=True,
            )
        else:
            _engine = create_engine(
                f"sqlite:///{db_cfg['sqlite_path']}",
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                future=True,
            )
    return _engine
