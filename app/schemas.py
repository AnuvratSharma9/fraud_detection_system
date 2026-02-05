from pydantic import BaseModel
from typing import Literal


class TransactionInput(BaseModel):
    type: Literal["PAYMENT", "TRANSFER", "DEBIT", "CREDIT"]
    amount: float

    oldbalanceOrg: float
    newbalanceOrig: float

    oldbalanceDest: float
    newbalanceDest: float


class PredictionResponse(BaseModel):
    fraud_probability: float
    risk_score: float
    risk_level: str
    action: str
    explanation: str
