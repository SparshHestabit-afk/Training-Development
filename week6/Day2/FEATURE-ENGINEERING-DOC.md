                                Hestabit Training Development
                                        Week 6 – Day 2

# Feature Engineering and Preprocessing

---

## Overview

The focus of Day 2 was to prepare the telecom churn dataset for machine learning by applying structured feature engineering and building a reusable preprocessing pipeline.

Rather than directly training a model on raw data, the objective was to:

* Derive meaningful behavioral features
* Convert categorical variables into machine-readable format
* Normalize numerical distributions
* Create a clean train-test split
* Save reusable artifacts for the next stages

This step ensures that the model training phase is both reliable and reproducible.

---

## Dataset Summary

The dataset contains customer-level telecom usage details such as:

* Call minutes across day, evening, night, and international periods
* Corresponding call charges
* Subscription plan information
* Customer service interaction counts
* Churn status (target variable)

### Target Variable

The `Churn` column is originally stored as a Boolean value:

* True → Customer churned
* False → Customer retained

For modeling purposes, it was converted into numerical form:

* 1 → Churn
* 0 → Not churn

This transformation allows compatibility with classification algorithms.

---

## Feature Engineering Approach

Instead of relying solely on raw usage statistics, additional features were created to capture broader behavioral patterns.

### Aggregated Usage Metrics

To represent overall activity, the following cumulative features were constructed:

* **Total_minutes** – Sum of all call minutes
* **Total_calls** – Sum of all call counts
* **Total_charge** – Sum of all billing charges

These features provide a consolidated view of customer engagement rather than fragmented time-based metrics.

---

### Behavioral Ratios and Efficiency Measures

Raw totals often fail to reflect intensity or proportional usage. To address this, normalized features were introduced:

* **Avg_minutes_per_call** – Average duration per call
* **Charge_per_minute** – Billing cost relative to total usage
* **Day_usage_ratio** – Share of daytime usage
* **Intl_usage_ratio** – Share of international usage

Ratio-based features tend to capture behavioral tendencies more effectively than absolute values.

---

### Customer Service Interaction Signal

Frequent customer service calls may indicate dissatisfaction or friction.

A derived binary feature, **High_service_calls**, was created:

* 1 → Above median number of service calls
* 0 → Otherwise

This simplifies detection of potentially dissatisfied customers.

---

### Plan Encoding

The following subscription indicators were converted from Yes/No to binary format:

* International plan
* Voice mail plan

Encoding:

* Yes → 1
* No → 0

This ensures compatibility with numerical modeling techniques while preserving interpretability.

---

## Preprocessing Pipeline

A structured preprocessing workflow was implemented using `scikit-learn` components to ensure consistency and reusability.

### Numerical Feature Treatment

Numerical variables were processed using:

1. **PowerTransformer** – To reduce skewness and stabilize variance
2. **StandardScaler** – To standardize features to zero mean and unit variance

This combination improves model stability and performance.

---

### Categorical Feature Treatment

Categorical variables were transformed using:

* **OneHotEncoder**

  * `handle_unknown="ignore"`
  * Dense output format

This ensures robustness when unseen categories appear in future data.

---

### ColumnTransformer Integration

Both numerical and categorical transformations were integrated into a unified `ColumnTransformer`.

This guarantees:

* Proper separation of feature types
* Consistent preprocessing across training and testing sets
* Prevention of data leakage

---

## Train-Test Split

The dataset was divided into training and testing sets using:

* 80% training data
* 20% testing data
* Fixed random seed for reproducibility
* Stratified splitting based on churn

Stratification ensures that both splits maintain similar class distribution, which is essential for reliable evaluation in classification tasks.

---

## Saved Artifacts

All intermediate outputs were stored in the `data/processed/` directory, including:

* X_train_full.npy
* X_test_full.npy
* y_train.npy
* y_test.npy
* preprocesser.pkl
* feature_name.pkl

Saving these artifacts allows the pipeline to remain modular. Feature selection and model training can now operate independently without re-running earlier steps.

---

### Key Takeaways

* Domain-driven feature construction can significantly enhance model input quality.
* Ratio-based features often provide stronger predictive signals than raw counts.
* Preprocessing pipelines must be fitted only on training data to avoid leakage.
* Stratified splitting is critical when working with classification problems.
* Persisting artifacts improves reproducibility and project structure.

---