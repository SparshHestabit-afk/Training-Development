import os
import joblib
import numpy as np
import json
import shap
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Paths of required directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
FEATURE_DIR = BASE_DIR / "features"
EVAL_DIR = BASE_DIR / "evaluation"

os.makedirs(EVAL_DIR, exist_ok=True)

# loading the data
X_train = np.load(DATA_DIR / "X_train_selected.npy")
X_test = np.load(DATA_DIR / "X_test_selected.npy")
y_test = np.load(DATA_DIR / "y_test.npy")
with open(FEATURE_DIR / "feature_list.json", "r") as f:
    feature_names = json.load(f)

# Converting to dataframe for shap
X_train_df = pd.DataFrame(X_train, columns=feature_names)
X_test_df = pd.DataFrame(X_test, columns=feature_names)

# Loading the tuned model
pipeline = joblib.load(MODELS_DIR / "tuned_model.pkl")
xgb_model = pipeline.named_steps["model"]


# SHAP analysis
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test_df)

plt.figure()
shap.summary_plot(shap_values, X_test_df, show=False)
plt.tight_layout()
plt.savefig(EVAL_DIR / "shap_summary.png")
plt.close()


# Feature Importance Plot
importances = xgb_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
plt.title("Feature Importances - Tuned XGBoost")
plt.tight_layout()
plt.savefig(EVAL_DIR / "feature_importance.png")
plt.close()

# Error Analysis Heatmap
y_pred = pipeline.predict(X_test_df)
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"])
plt.title("Confusion Matrix Heatmap")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(EVAL_DIR / "error_heatmap.png")
plt.close()

print("\n===============")
print("SHAP Summary, Feature Importance, and Error Heatmap saved")
print("===============\n")