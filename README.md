# Fraud Detection System

A machine learning system that detects fraudulent financial transactions in real-time using Random Forest classification and provides AI-powered explanations for each prediction.

## Overview

This project predicts the probability of a transaction being fraudulent and assigns a risk level (High/Medium/Low). It consists of:

- **Backend API** (FastAPI) - Serves ML model predictions
- **Frontend UI** (Streamlit) - Interactive web interface for testing transactions
- **ML Model** (Random Forest) - Trained on financial transaction data
- **LLM Integration** (Groq) - Generates human-readable explanations

## Features

- Real-time fraud probability prediction
- Risk scoring and classification
- Natural language explanations for predictions
- RESTful API with automatic documentation
- Interactive web interface

## Tech Stack

- **ML**: Scikit-learn, Random Forest
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **LLM**: Groq API
- **Deployment**: Render

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/AnuvratSharma9/fraud-detection-system.git
cd fraud-detection-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from groq

## Usage

### Run the Backend API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Run the Frontend (in a new terminal)

```bash
streamlit run frontend.py
```

The web interface will open at `http://localhost:8501`

### Make a Prediction via API

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TRANSFER",
    "amount": 50000,
    "oldbalanceOrg": 100000,
    "newbalanceOrig": 50000
  }'
```

## API Endpoints

- `GET /health` - Check API status
- `POST /predict` - Predict fraud probability

### Request Body
```json
{
  "type": "TRANSFER",
  "amount": 50000.00,
  "oldbalanceOrg": 100000.00,
  "newbalanceOrig": 50000.00,
  "oldbalanceDest":1000002.00,
  "newbalanceDest":500000.00
}
```

### Response
```json
{
  "fraud_probability": 0.89,
  "risk_score": 89,
  "risk_level": "High",
  "prediction": "Fraudulent",
  "explanation": "This transaction shows high fraud risk..."
}
```

## Project Structure

```
fraud-detection-system/
├── app/
│   ├── main.py           # FastAPI application
│   ├── schemas.py        # Pydantic models
│   └── model.py          # ML model loading
├── models/
│   └── rf_pipe.pkl   # Trained model
├── frontend.py           # Streamlit app
├── requirements.txt      # Dependencies
└── README.md
```

