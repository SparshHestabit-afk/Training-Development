from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

#PATHS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR/"data"/"raw"/"telcom_churn.csv"
OUTPUT_DIR = BASE_DIR/"data"/"processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#LOADING DATA

def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df

#Featured Engineering

def create_new_features(df):
    df = df.copy()

    df["Total_minutes"] = (
        df["Total day minutes"] +
        df["Total eve minutes"] +
        df["Total night minutes"] +
        df["Total intl minutes"]
    )

    df["Total_calls"] = (
        df["Total day calls"] +
        df["Total eve calls"] +
        df["Total night calls"] +
        df["Total intl calls"]
    )

    df["Avg_minutes_per_call"] = df["Total_minutes"] / (df["Total_calls"] + 1)

    df["Total_charge"] = (
        df["Total day charge"] +
        df["Total eve charge"] +
        df["Total night charge"] +
        df["Total intl charge"]
    )

    df["Charge_per_minute"] = df["Total_charge"] / (df["Total_minutes"] + 1)

    df["Day_usage_ratio"] = df["Total day minutes"] / (df["Total_minutes"] + 1)

    df["Intl_usage_ratio"] = df["Total intl minutes"] / (df["Total_minutes"] + 1)

    df["High_service_calls"] = (
        df["Customer service calls"] > df["Customer service calls"].median()
    ).astype(int)

    df["International plan"] = df["International plan"].map({"Yes": 1, "No": 0})

    df["Voice mail plan"] = df["Voice mail plan"].map({"Yes": 1, "No": 0})

    return df


def build_preprocesser(X):

    categorical_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=["object", "string"]).columns.tolist()

    numeric_pipeline = Pipeline([
        ("power", PowerTransformer()),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numerical_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ])

    return preprocessor, numerical_cols, categorical_cols


def main():

    df = load_data()
    df = create_new_features(df)

    y = df["Churn"].astype(int)
    X = df.drop(columns=["Churn"])

    preprocessor, num_cols, cat_cols = build_preprocesser(X)

    print("NaN in Churn:", df["Churn"].isna().sum())
    print(df["Churn"].unique())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    cat_features = (
        preprocessor.named_transformers_["cat"]
        .named_steps["onehot"]
        .get_feature_names_out(cat_cols)
    )

    feature_names = num_cols + list(cat_features)

    np.save(OUTPUT_DIR / "X_train_full.npy", X_train_processed)
    np.save(OUTPUT_DIR/ "X_test_full.npy", X_test_processed)
    np.save(OUTPUT_DIR/ "y_train.npy", y_train)
    np.save(OUTPUT_DIR/ "y_test.npy", y_test)

    joblib.dump(preprocessor, OUTPUT_DIR / "preprocesser.pkl")
    joblib.dump(feature_names, OUTPUT_DIR / "feature_name.pkl")

    print("Feature Engineering Completed Successfully")


if __name__ == "__main__":
    main()