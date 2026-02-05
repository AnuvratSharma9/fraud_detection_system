from fastapi import FastAPI
from app.explainer import generate_explanation
import pandas as pd
import numpy as np


from app.schemas import TransactionInput, PredictionResponse
from models.model import fraud_model
from app.decision import get_risk_level, get_action

app = FastAPI(
    title="Fraud Risk Decision API",
    description="API for fraud risk scoring and decisioning",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(tx: TransactionInput):
        log_amount = np.log1p(tx.amount)

        balance_diff_orig = tx.oldbalanceOrg - tx.newbalanceOrig
        balance_diff_dest = tx.newbalanceDest - tx.oldbalanceDest

        X = pd.DataFrame([{
    "type": tx.type,
    "log_amount": log_amount,
    "balance_diff_orig": balance_diff_orig,
    "balance_diff_dest": balance_diff_dest
}])

        prob = fraud_model.predict_proba(X)
        risk_score = prob * 100

        if prob > 0.8:
            risk_level = "HIGH"
            action = "BLOCK"
        elif prob > 0.4:
            risk_level = "MEDIUM"
            action = "REVIEW"
        else:
            risk_level = "LOW"
            action = "ALLOW"

        explanation = generate_explanation(
    tx,
    amount=tx.amount,
    fraud_probability=prob,
    risk_level=risk_level,
    action=action
)


        return PredictionResponse(
    fraud_probability=prob,
    risk_score=risk_score,
    risk_level=risk_level,
    action=action,
    explanation=explanation
)

        