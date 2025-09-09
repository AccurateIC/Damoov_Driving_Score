# db_utils.py
from sqlalchemy import create_engine
from pathlib import Path

def get_engine(config):
    db = config['database']
    if db['type'].lower() == 'mysql':
        user = db['user']
        pwd = db['password']
        host = db['host']
        port = db.get('port', 3306)
        name = db['name']
        # PyMySQL driver
        url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset=utf8mb4"
        return create_engine(url, pool_pre_ping=True, pool_recycle=3600)
    else:
        # SQLite
        sqlite_path = Path(db['sqlite_path'])
        return create_engine(f"sqlite:///{sqlite_path}")
