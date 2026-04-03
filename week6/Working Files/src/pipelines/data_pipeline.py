import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../"))

RAW_PATH = os.path.join(PROJECT_ROOT, "data/raw/telcom_churn.csv")
PROCESSED_PATH = os.path.join(PROJECT_ROOT, "data/processed/final.csv")

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    # removing duplicates
    df = df.drop_duplicates()

    # handling missing values
    # df = df.dropna()
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include=['object', 'string', 'category']).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    #handling outliers (IQR capping)
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df[col] = df[col].clip(lower_bound, upper_bound)
    
    return df

#class-imbalance check
def check_class_imbalance(df, target_column="Churn"):
    if target_column not in df.columns:
        print(f"Target column '{target_column}' not found.")
        return

    class_counts = df[target_column].value_counts()
    class_percent = df[target_column].value_counts(normalize=True) * 100

    print("\nClass Distribution:")
    print(class_counts)

    print("\nClass Percentage:")
    print(class_percent)

    minority_class_percentage = class_percent.min()

    if minority_class_percentage < 20:
        print("\n Warning: Dataset is strongly imbalanced.")
    elif minority_class_percentage < 30:
        print("\n Warning: Dataset is moderately imbalanced.")
    else:
        print("\n Dataset is reasonably balanced.")

def save_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df = load_data(RAW_PATH)
    df = clean_data(df)

    check_class_imbalance(df, target_column="Churn")

    save_data(df, PROCESSED_PATH)

    print("Data Loaded")
    print("Cleaned dataset saved")
    print("EDA report generated")