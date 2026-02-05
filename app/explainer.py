import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def _fallback_explanation(tx_type, amount, fraud_probability, risk_level, action):
    """
    Safe fallback if LLM fails or API key missing.
    This guarantees your API NEVER breaks.
    """
    return (
        f"This transaction is classified as {risk_level} risk. "
        f"The transaction type is {tx_type}, and the amount ({amount:.2f}) "
        f"is significantly higher than typical values. "
        f"The model predicts a fraud probability of {fraud_probability:.0%}, "
        f"which justifies the recommended action: {action}."
    )


def generate_explanation(
    tx_type: str,
    amount: float,
    fraud_probability: float,
    risk_level: str,
    action: str,
) -> str:
    """
    Generates a human-readable explanation using Groq LLM.
    Falls back to deterministic explanation if LLM is unavailable.
    """

    # If API key is missing, do NOT crash
    if not GROQ_API_KEY:
        return _fallback_explanation(
            tx_type, amount, fraud_probability, risk_level, action
        )

    prompt = f"""
You are a senior fraud risk analyst at a fintech company.

Explain WHY the following transaction is classified as {risk_level} risk.
Be specific, business-oriented, and reference the numeric values.

Transaction details:
- Transaction type: {tx_type}
- Amount: {amount}
- Fraud probability predicted by model: {fraud_probability:.2%}
- Final risk level: {risk_level}
- Recommended action: {action}

Explain clearly:
1. Why the amount is risky or not
2. Why this transaction type matters
3. How the probability influenced the decision
4. Why the action makes sense

Write in 4–6 clear sentences. Do NOT mention AI, models, or probabilities explicitly.
"""

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You explain fraud decisions to business users."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 250,
        }

        response = requests.post(
            GROQ_URL, headers=headers, json=payload, timeout=15
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception:
        # Absolute safety net
        return _fallback_explanation(
            tx_type, amount, fraud_probability, risk_level, action
        )
