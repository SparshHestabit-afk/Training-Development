import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import entropy

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASELINE_PATH = os.path.join(BASE_DIR, "artifacts", "training_baseline.csv")
LIVE_LOG_PATH = os.path.join(BASE_DIR, "logs", "prediction_logs.csv")
REPORT_PATH = os.path.join(BASE_DIR, "logs", "drift_report.json")

# PSI calculation function
def calculate_psi(expected, actual, buckets=10):
    """
    Calculate Population Stability Index (PSI)
    """

    expected = np.array(expected)
    actual = np.array(actual)

    # create equal percentile bins based on expected data
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))

    expected_counts = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    actual_counts = np.histogram(actual, bins=breakpoints)[0] / len(actual)

    # avoiding division by zero
    epsilon = 1e-6
    psi_values = (actual_counts - expected_counts) * np.log(
        (actual_counts + epsilon) / (expected_counts + epsilon)
    )

    return np.sum(psi_values)


def drift_check():

    if not os.path.exists(BASELINE_PATH):
        print("Baseline file not found.")
        return
    
    if not os.path.exists(LIVE_LOG_PATH):
        print("Live log file not found")
        return
    
    baseline = pd.read_csv(BASELINE_PATH)
    live_logs = pd.read_csv(LIVE_LOG_PATH)

    if live_logs.shape[0] <10:
        print("Not enough live data for reliable drift detection")
        return
    
    # Removing non-feature columns
    drop_cols = ["request_id", "timestamp", "model_version", "probability", "prediction"]
    live_logs = live_logs.drop(columns=[col for col in drop_cols if col in live_logs.columns])

    print("\n=====================")
    print("Drift report (PSI Based)")
    print("=====================\n")

    numeric_columns = baseline.select_dtypes(include=[np.number]).columns

    drift_results = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_live_records": int(live_logs.shape[0]),
        "features":{}
    }

    drift_detected = False

    for column in numeric_columns:
        if column not in live_logs.columns:
            continue

        psi_score = calculate_psi(baseline[column], live_logs[column])

        if psi_score < 0.1:
            status = "No Drift"
        elif psi_score < 0.2:
            status = "Moderate Drift"
            drift_detected = True
        else:
            status = "Major Drift"
            drift_detected = True

        drift_results["features"][column] = {
            "PSI": round(float(psi_score), 4),
            "status": status
        }
    drift_results["system_status"] = (
        "Drift Detected" if drift_detected else "No Drift Detected (STABLE)"
    )

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            existing_report = json.load(f)
    else:
        existing_report = []

    existing_report.append(drift_results)

    with open(REPORT_PATH, "w") as f:
        json.dump(existing_report, f, indent=4)

    return drift_results
    
    print("\n Drift check completed successfully")


# Running Script for the drift check
if __name__ == "__main__":
    drift_check()