import streamlit as st
import requests
import pandas as pd
import math

BACKEND_URL = "https://fraud-detection-system-back.onrender.com/predict"  
st.set_page_config(page_title="Fraud Risk Analysis", layout="wide")

st.title("💳 Fraud Risk Analysis")
st.caption("ML-powered fraud detection with LLM explanations")
#SIDE BAR
st.sidebar.header("Transaction Details")

tx_type = st.sidebar.selectbox(
    "Transaction Type",
    ["PAYMENT", "TRANSFER", "DEBIT"]
)

amount = st.sidebar.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.sidebar.number_input("Old Balance (Origin)", min_value=0.0, value=5000.0)
newbalanceOrig = st.sidebar.number_input("New Balance (Origin)", min_value=0.0, value=4000.0)

oldbalanceDest = st.sidebar.number_input("Old Balance (Destination)", min_value=0.0, value=2000.0)
newbalanceDest = st.sidebar.number_input("New Balance (Destination)", min_value=0.0, value=3000.0)

analyze = st.sidebar.button("🔍 Analyze Transaction")

# ---------------- API Call ----------------
if analyze:
    payload = {
        "type": tx_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    try:
        res = requests.post(BACKEND_URL, json=payload)
        res.raise_for_status()
        data = res.json()

        
        col1, col2, col3 = st.columns(3)

        col1.metric("Fraud Probability", f"{data['fraud_probability']*100:.2f}%")
        col2.metric("Risk Level", data["risk_level"])
        col3.metric("Action", data["action"])

        st.divider()

        
        st.subheader("📊 Risk Contribution Breakdown")

        log_amount = math.log1p(amount)
        balance_diff_orig = oldbalanceOrg - newbalanceOrig
        balance_diff_dest = newbalanceDest - oldbalanceDest

        df = pd.DataFrame({
            "Feature": ["Log Amount", "Balance Diff (Orig)", "Balance Diff (Dest)"],
            "Value": [log_amount, balance_diff_orig, balance_diff_dest]
        })

        st.bar_chart(df.set_index("Feature"))

        st.subheader("💰 Transaction Amount vs Normal Range")

        range_df = pd.DataFrame({
            "Category": ["This Transaction", "Typical Safe Limit"],
            "Amount": [amount, 250000]
        })

        st.bar_chart(range_df.set_index("Category"))

        st.subheader("🧠 LLM Explanation")
        st.success(data["explanation"])

    except Exception as e:
        st.error(f"Backend error: {e}")
