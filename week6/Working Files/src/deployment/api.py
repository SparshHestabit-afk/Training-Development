from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from uuid import uuid4
from datetime import datetime
from monitoring.drift_checker import drift_check

import os
import json
import joblib
import pandas as pd

# Loading environment variables and intial setup
load_dotenv()

app = FastAPI(
    title="Customer Churn Prediction API",
    description="An API for predicting customer churn using a pre-trained machine learning model.",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
MODEL_PATH = f"artifacts/best_model_{MODEL_VERSION}.pkl"
FEATURE_PATH = f"artifacts/feature_list_{MODEL_VERSION}.json"
JSON_LOG_PATH = os.path.join(LOG_DIR, "prediction_logs.json")
CSV_LOG_PATH = os.path.join(LOG_DIR, "prediction_logs.csv")
THRESHOLD = float(os.getenv("THRESHOLD", 0.5))
drift_threshold = 20

# LOADING MODEL AND FEATURE LIST
try:
    model= joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

try:
    with open(FEATURE_PATH,"r") as f:
        feature_list = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load feature list: {e}")


# schema for input data(request)
class ChurnRequest(BaseModel):
    data: dict

# health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "OK, API is running",
        "model_version": MODEL_VERSION
    }

# prediction endpoint
@app.post("/predict")
def predict_churn(request: ChurnRequest):

    request_id = str(uuid4())
    input_data = request.data

    # checking for missing features
    missing_features = [f for f in feature_list if f not in input_data]
    if missing_features:
        raise HTTPException(
            status_code=400,
            detail=f"Missing Required Features: {missing_features}"
        )
    
    ordered_values = [input_data[f] for f in feature_list]
    input_df = pd.DataFrame([ordered_values], columns=feature_list)

    try:
        probability = model.predict_proba(input_df)[0][1]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail = f"Prediction failed: {str(e)}"
        )
    
    prediction = int(probability >= THRESHOLD)
    log_df = pd.read_csv(CSV_LOG_PATH)
    
    if len(log_df) %drift_threshold == 0:
        drift_check()

    # logging the prediction request and response
    log_prediction(
        request_id= request_id,
        features = input_data,
        probability = probability,
        prediction = prediction
    )

    return {
        "request_id": request_id,
        "probability": float(round(probability, 4)),
        "prediction": int(prediction),
        "model_version": MODEL_VERSION
    }

@app.get("/monitor/drift")
def run_drift():
    return drift_check()

# logging function
def log_prediction(request_id, features, probability, prediction):

    log_entry = {
        "request_id": request_id,
        "timestamp": datetime.utcnow().isoformat(),
        "model_version": MODEL_VERSION,
        "probability": float(probability),
        "prediction": int(prediction),
        **features
    }

    with open(JSON_LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    log_df = pd.DataFrame([log_entry])

    if not os.path.exists(CSV_LOG_PATH) or os.stat(CSV_LOG_PATH).st_size == 0:
        log_df.to_csv(CSV_LOG_PATH, index=False)
    else:
        log_df.to_csv(CSV_LOG_PATH, mode="a", header=False, index=False)