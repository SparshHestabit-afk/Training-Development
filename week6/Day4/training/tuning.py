import os 
import json
import joblib
import numpy as np
import optuna

from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

from xgboost import XGBClassifier

# Paths of required directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
TUNING_DIR = BASE_DIR / "tuning"

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TUNING_DIR, exist_ok=True)

# Loading the data
X_train = np.load(DATA_DIR / "X_train_selected.npy")
y_train = np.load(DATA_DIR / "y_train.npy")

neg, pos = np.bincount(y_train)
scale_pos_weight = neg / pos

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Optuna objective function for hyperparameter tuning
def objective(trial):
    
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 300, 1000),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.02),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "gamma": trial.suggest_float("gamma", 0.0, 1.0),
        "reg_lambda": trial.suggest_float("reg_lambda", 1.0, 10.0),
        "scale_pos_weight": scale_pos_weight,
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "random_state": 42,
        "n_jobs": -1
    }

    pipeline = Pipeline([
        ("smote", SMOTE(random_state=42)),
        ("model", XGBClassifier(**params))
    ])

    scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    )

    return scores.mean()


# run optuna optimization
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=25)

best_params = study.best_params
best_score = study.best_value

# training final tuned model
best_params.update({
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "random_state": 42,
    "n_jobs": -1
})

final_pipeline = Pipeline([
    ("smote", SMOTE(random_state=42)),
    ("model", XGBClassifier(**best_params))
])

final_pipeline.fit(X_train, y_train)

joblib.dump(final_pipeline, MODELS_DIR / "tuned_model.pkl")


# sacing the tuning results
results = {
    "best_params": best_params,
    "best_cv_score": best_score
}

with open(TUNING_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=4)


print("\n===============")
print("Best CV ROC-AUC:", best_score)
print("Best Parameters:", best_params)
print("Tuning completed successfully")
print("===============\n")