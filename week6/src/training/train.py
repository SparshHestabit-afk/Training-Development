import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import cross_validate
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.preprocessing import StandardScaler

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier


# Creating required directories

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
EVAL_DIR = BASE_DIR / "evaluation"
FEATURE_DIR = BASE_DIR / "features" / "feature_list.json"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

# Loading the processed data
X_train = np.load(DATA_DIR / "X_train_selected.npy")
X_test = np.load(DATA_DIR /"X_test_selected.npy")
y_train = np.load(DATA_DIR / "y_train.npy")
y_test = np.load(DATA_DIR / "y_test.npy")

neg, pos = np.bincount(y_train)
scale_pos_weight = neg / pos

# Defining the models to be trained
models = {
    "Logistic Regression": Pipeline([
        ("smote", SMOTE(random_state=42)),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=2000,
            solver="lbfgs",
            C=1.0,
            class_weight=None,
            random_state=42
        ))
    ]),

    "Random Forest": Pipeline([
        ("smote", SMOTE(random_state=42)),
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(
            n_estimators=400,
            max_depth=None,
            min_samples_split=2,
            n_jobs=-1,
            random_state=42
        ))
    ]),

    "XGBoost": Pipeline([
        ("smote", SMOTE(random_state=42)),
        ("scaler", StandardScaler()),
        ("model", XGBClassifier(
           objective= "binary:logistic",
            eval_metric= "logloss",
            n_estimators=400,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1
        ))
    ]),

    "Neural Network": Pipeline([
        ("smote", SMOTE(random_state=42)),
        ("scaler", StandardScaler()),
        ("model", MLPClassifier(
            hidden_layer_sizes=(128,64),
            activation="relu",
            alpha=0.001,
            max_iter=1000,
            random_state=42
        ))
    ])
}


# Cross-validation and model training
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scoring= {
    "accuracy":"accuracy",
    "precision":"precision",
    "recall":"recall",
    "f1":"f1",
    "roc_auc":"roc_auc"
}

metrics_results = {}
best_model_name = None
best_roc_auc = 0


for name, pipeline in models.items():

    cv_results = cross_validate(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
        n_jobs=-1
    )

    avg_metrics = {
        metric: float(np.mean(cv_results[f"test_{metric}"]))
        for metric in scoring
    }

    metrics_results[name] = avg_metrics

    if avg_metrics["roc_auc"] > best_roc_auc:
        best_roc_auc = avg_metrics["roc_auc"]
        best_model_name = name


# Trainng the best model 
best_pipeline = models[best_model_name]
best_pipeline.fit(X_train, y_train)

joblib.dump(best_pipeline, MODELS_DIR / "best_model.pkl")


# final evaluation
y_pred = best_pipeline.predict(X_test)
y_prob = best_pipeline.predict_proba(X_test)[:, 1]

test_metrics = {
    "accuracy": float(accuracy_score(y_test, y_pred)),
    "precision": float(precision_score(y_test, y_pred)),
    "recall": float(recall_score(y_test, y_pred)),
    "f1": float(f1_score(y_test, y_pred)),
    "roc_auc": float(roc_auc_score(y_test, y_prob))
}

metrics_results["best_model"] = best_model_name
metrics_results["test_metrics"] = test_metrics


# saving metrics results
with open(EVAL_DIR / "metric.json", "w") as f:
    json.dump(metrics_results, f, indent=4)


# confusion matrix plot
disp = ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
plt.title(f"Confusion Matrix - {best_model_name}")
plt.savefig(EVAL_DIR / "confusion_matrix.png")
plt.close()

print("\n====================")
print(f"Best Model: {best_model_name}")
print("Training Completed Successfully")
print("====================\n")


MODEL_VERSION = "v1"
os.makedirs("artifacts", exist_ok=True)
joblib.dump(best_pipeline, f"artifacts/best_model_{MODEL_VERSION}.pkl")
with open(FEATURE_DIR, "r") as f:
    feature_list = json.load(f)

with open(f"artifacts/feature_list_{MODEL_VERSION}.json", "w") as f:
    json.dump(feature_list, f, indent=4)

print(f"Model and feature list saved successfully")

baseline_df = pd.DataFrame(X_train, columns=feature_list)
baseline_df.to_csv(f"artifacts/training_baseline.csv", index=False)

print("Baseline training data saved successfully")