                                Hestabit Training Development
                                        Week 6 - Day 5

# Deployment Guide

## Introduction

This document describes the deployment process for the Machine Learning API.
The application exposes a prediction service along with an integrated data drift monitoring system.

The deployment is containerized using Docker and includes:

- FastAPI inference service
- Serialized trained model
- Prediction logging
- Automated PSI-based drift detection
- Persistent monitoring reports

The objective is to simulate a production-ready MLOps deployment workflow.

---

## System Components

The deployed system consists of the following components:

1. **Model Artifact**
   - Serialized model file stored in `artifacts/`
   - Baseline training distribution saved for drift comparison

2. **Inference Service**
   - FastAPI application (`api.py`)
   - `/predict` endpoint for model inference
   - Structured logging of predictions

3. **Monitoring Module**
   - PSI-based drift detection (`monitoring/drift_checker.py`)
   - Manual trigger endpoint: `/monitor/drift`
   - Automatic drift execution after a defined number of predictions
   - Historical drift reports stored in JSON format

4. **Persistent Logs**
   - `prediction_logs.csv`
   - `drift_report.json`

---

## Prerequisites

Ensure the following tools are installed:

- Docker
- Python 3.9 or higher
- pip
- Git

Optional (recommended for API testing):
- Postman
- cURL

---

## Local Setup (Without Docker)

Clone the repository:

```
git clone <repository-url>
cd week6
````

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Start the API server:

```
uvicorn main:app --host 0.0.0.0 --port 8001:8000
```

Access the application at:

```
http://localhost:8001
```

Swagger documentation will be available at:

```
http://localhost:8000/docs
```

---

## Docker Deployment

### Build Docker Image

```
docker build -t churn-api:v1 .
```

### Run the Container

```bash
docker run -p 8000:8000 churn-api:v1
```

The API will now be accessible at:

```
http://localhost:8000
```

---

## API Endpoints

### Prediction Endpoint

```
POST /predict
```

Functionality:

* Accepts structured feature input
* Returns predicted class and probability
* Logs request metadata and prediction result
* Automatically checks whether drift monitoring should be triggered

Successful response returns HTTP 200.

---

### Drift Monitoring Endpoint

```
GET /monitor/drift
```

Functionality:

* Compares live prediction data with training baseline
* Calculates PSI for numeric features
* Determines drift severity (No Drift / Moderate / Major)
* Appends structured results to `drift_report.json`

---

##Automated Drift Workflow

The monitoring system is configured to run automatically after a predefined number of predictions.

Execution flow:

1. Prediction request is received
2. Input and output are logged
3. Log size is evaluated
4. If threshold is reached:

   * Drift detection runs automatically
   * Report is appended to JSON file
   * System status is updated

This ensures continuous monitoring without manual intervention.

---

## Log and Report Storage

### Prediction Logs

Location:

```
logs/prediction_logs.csv
```

Contains:

* Request ID
* Timestamp
* Model version
* Feature values
* Prediction
* Probability score

---

### Drift Reports

Location:

```
logs/drift_report.json
```

Each drift entry contains:

* Execution timestamp
* Total live samples
* Feature-level PSI values
* Drift status per feature
* Overall system status

Reports are appended, allowing historical tracking.

---

## Deployment Verification Checklist

Before considering deployment complete, verify:

* Docker image builds successfully
* Container runs without errors
* `/predict` returns HTTP 200
* Predictions are logged correctly
* `/monitor/drift` returns structured JSON
* Drift report file updates after execution
* Automatic drift trigger works as configured

---
