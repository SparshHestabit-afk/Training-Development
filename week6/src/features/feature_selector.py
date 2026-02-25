import json
from pathlib import Path
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR/ "data"/"processed"
FEATURE_FILE = BASE_DIR/ "features"/"feature_list.json"

def load_data():
    X_train = np.load(OUTPUT_DIR /"X_train_full.npy")
    X_test = np.load(OUTPUT_DIR /"X_test_full.npy")
    y_train = np.load(OUTPUT_DIR /"y_train.npy")
    y_test = np.load(OUTPUT_DIR /"y_test.npy")
    feature_names = joblib.load(OUTPUT_DIR /"feature_name.pkl")

    return X_train, X_test, y_train, y_test, feature_names

def correlation_filter(X, threshold=0.9):

    corr_matrix = np.corrcoef(X, rowvar=False)
    upper = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)

    to_drop = [
        i for i in range(corr_matrix.shape[0])
        if any(abs(corr_matrix[i][j]) > threshold and upper[i][j]
               for j in range(corr_matrix.shape[1]))
    ]

    keep_indices = [i for i in range(X.shape[1]) if i not in to_drop]
    return keep_indices


def mutual_information_selection(X, y, k=20):
    mi = mutual_info_classif(X, y, random_state=42)
    return np.argsort(mi)[-k:]

def rfe_selection(X, y, n_features=20):
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    selector = RFE(model, n_features_to_select=n_features)
    selector.fit(X, y)
    return np.where(selector.support_)[0]

def plot_importance(X, y, feature_names):

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    importances = model.feature_importances_
    indices = np.argsort(importances)[-15:]

    plt.figure()
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), np.array(feature_names)[indices])
    plt.title("Top 15 Feature Importances")
    plt.tight_layout()
    # plt.show()
    plt.savefig(OUTPUT_DIR / "feature_importance.png", bbox_inches="tight")
    plt.close()



def main():

    X_train, X_test, y_train, y_test, feature_names = load_data()

    keep_corr = correlation_filter(X_train, threshold=0.95)
    X_train_corr = X_train[:, keep_corr]
    X_test_corr = X_test[:, keep_corr]

    mi_indices = mutual_information_selection(X_train_corr, y_train, k=25)

    final_indices = np.array(keep_corr)[mi_indices]

    X_train_selected = X_train[:, final_indices]
    X_test_selected = X_test[:, final_indices]
    
    selected_features = [feature_names[i] for i in final_indices]

    np.save(OUTPUT_DIR / "X_train_selected.npy", X_train_selected)
    np.save(OUTPUT_DIR / "X_test_selected.npy", X_test_selected)

    with open(FEATURE_FILE, "w") as f:
        json.dump(selected_features, f, indent=4)
    
    print(f"Selected {len(selected_features)} features.")
    
    plot_importance(X_train_selected, y_train, selected_features)

if __name__ == "__main__":
    main()