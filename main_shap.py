
from shap_model import XGBConfig, XGBoostModelTrainer

config = XGBConfig(
    db_path="csv/tracking_raw_DB_150525 (2).db",          # 🔁 Set your actual DB file name
    table_name="SampleTable"    # 🔁 Set your actual table name
)

trainer = XGBoostModelTrainer(config)
trainer.train()
