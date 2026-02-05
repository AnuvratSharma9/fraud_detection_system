import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "rf.pkl"

class FraudModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[0, 1]

fraud_model = FraudModel()
