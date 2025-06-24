"""
from lstm_model import LSTMConfig, LSTM_HMM_Model
from sklearn.metrics import r2_score

if __name__ == "__main__":
    config = LSTMConfig(
        db_path="csv/raxel_traker_db_200325 (1).db",
        table_name="SampleTable",
        sequence_length=60
    )

    model = LSTM_HMM_Model(config)
    model.train_lstm()
    model.train_hmm()

    results = model.predict_for_all_trips()
    for res in results:
        print(res)

"""
from lstm_model import Config, LSTM_HMM_Trainer

if __name__ == "__main__":
    config = Config(
        db_path="csv/tracking_raw_DB_150525 (2).db",
        table_name="SampleTable",
        sequence_length=60
    )

    trainer = LSTM_HMM_Trainer(config)
    trainer.train_lstm()  # Train and evaluate LSTM (per-trip regression)

    trainer.train_hmm()   # Train HMM on trip sequences
    results = trainer.predict_driver_behaviors()

    for r in results:
        print(r)

