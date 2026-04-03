import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"

# =========================
# Load Data
# =========================

X_test = np.load(DATA_DIR / "X_test_selected.npy")
y_test = np.load(DATA_DIR / "y_test.npy")

# =========================
# Load Tuned Model
# =========================

model = joblib.load(MODELS_DIR / "tuned_model.pkl")

# =========================
# Predictions
# =========================

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# =========================
# Metrics
# =========================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("\n===== Tuned Model Test Performance =====")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
