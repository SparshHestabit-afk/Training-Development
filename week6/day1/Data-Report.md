**Week 6 – Day 1**

# Project Objective

Customer churn prediction is a critical problem in the telecom industry. Retaining existing customers is significantly more cost-effective than acquiring new ones.

The objective of this phase was to:

* Understand the dataset structure
* Perform systematic data validation
* Detect missing values and duplicates
* Analyze feature distributions
* Identify outliers
* Examine class imbalance
* Generate meaningful insights before modeling

Rather than rushing into model building, the focus was placed on building a strong and interpretable data foundation.

---

## Dataset Overview

**Dataset Name:** `telcom_churn.csv`
**Rows:** 2666
**Columns:** 20

The dataset contains telecom customer activity information along with a churn indicator.

### Feature Categories

**Customer Information**

* `State`
* `Area code`
* `Account length`

**Subscription Plans**

* `International plan`
* `Voice mail plan`

**Usage Metrics**

* Total day minutes / calls / charge
* Total evening minutes / calls / charge
* Total night minutes / calls / charge
* Total international minutes / calls / charge

**Service Interaction**

* `Customer service calls`

**Target Variable**

* `Churn` (True / False)

![Dataset Overview](../Screenshots/day1/dataset_overview.png)

---

## Initial Data Inspection

The dataset was examined using:

* `df.head()`
* `df.shape`

![Dataset overview HEAD + SHAPE inspection](../Screenshots/day1/dataset_overview_2.png)

* `df.info()`

![Dataset overview INFO inspection](../Screenshots/day1/dataset_overview_3.png)

* `df.describe()`
* `df.describe(include=['object','string'])`

![Dataset overview HEAD + SHAPE inspection](../Screenshots/day1/dataset_overview_4.png)

### Key Observations

* No major datatype inconsistencies.
* Numeric and categorical features are clearly separated.
* Usage-based charge columns are proportional to their respective minute columns.

---

## Missing Value Analysis

```
df.isnull().sum()
```

A heatmap was also generated for visual inspection.

![ IMAGE SPACE – Missing Value Heatmap ](../Screenshots/day1/missing_value_analysis.png)
![ IMAGE SPACE – Missing Value Heatmap ](../Screenshots/day1/missing_value_analysis_2.png)


### Observation

* No significant missing values were detected.
* Dataset integrity is preserved.

---

## Duplicate Check

```
df.duplicated().sum()
```

### Observation

* No duplicate rows found.
* Dataset does not contain redundant entries.

![Duplicate check](../Screenshots/day1/duplicate_check.png)

---

## Target Variable Analysis (Churn)

```
df['Churn'].value_counts()
df['Churn'].value_counts(normalize=True)
```

### Distribution:

* **Non-Churn:** 2278 customers (~85.45%)
* **Churn:** 388 customers (~14.55%)

![ IMAGE SPACE – Target Distribution Bar Chart ](../Screenshots/day1/target_distribution.png)

![ IMAGE SPACE – Target Distribution Bar Chart ](../Screenshots/day1/target_distribution_2.png)


### Interpretation

The dataset shows a moderate class imbalance. With only ~15% churn cases, accuracy alone would not be a reliable evaluation metric during modeling.

Future modeling will prioritize:

* Precision
* Recall
* F1-score
* ROC-AUC

---

## Feature Distribution Analysis

Histograms with KDE were generated for all numeric features.

```
sns.histplot(df[col], kde=True)
```

![ IMAGE SPACE – Sample Feature Distribution ](../Screenshots/day1/feature_distribution.png)

![ IMAGE SPACE – Sample Feature Distribution ](../Screenshots/day1/feature_distribution_2.png)

![ IMAGE SPACE – Sample Feature Distribution ](../Screenshots/day1/feature_distribution_3.png)

![ IMAGE SPACE – Sample Feature Distribution ](../Screenshots/day1/feature_distribution_4.png)


### Key Observations

* Usage-related features show near-normal distribution.
* Customer service calls exhibit slight right skew.
* No extreme abnormal patterns observed in raw distributions.

---

## Correlation Analysis

## 8.1 Correlation Matrix

```
sns.heatmap(df[numeric_cols].corr(), cmap="viridis")
```

![ IMAGE SPACE – Correlation Heatmap ](../Screenshots/day1/correlation_matrix.png)

### Observations

* Strong correlation between:
  * Minutes and their corresponding charge columns
* Moderate relationships among usage patterns
* No severe multicollinearity beyond expected proportional relationships

---

## 8.2 Correlation with Target (Churn)

```
df.corr(numeric_only=True)['Churn'].sort_values(ascending=False)
```

![ IMAGE SPACE – Correlation Heatmap ](../Screenshots/day1/correlation_matrix_2.png)


### Notable Signals

* Customer service calls show noticeable association with churn.
* Certain usage behaviors influence churn probability.
* Charge columns mirror their respective minute correlations.

---

## Outlier Analysis

Outliers were examined using the **Interquartile Range (IQR) method**.

### IQR Formula

```
IQR = Q2 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q2 + 1.5 × IQR
```

![ IMAGE SPACE – Boxplot Example (Total Day Minutes) ](../Screenshots/day1/Outliers.png)

Quantitative outlier counts were computed for all numeric columns.

### Boxplot Visualization

```
sns.boxplot(x=df[col])
```

![ IMAGE SPACE – Boxplot Example (Total Day Minutes) ](../Screenshots/day1/Outliers_2.png)

![ IMAGE SPACE – Boxplot Example (Total Day Minutes) ](../Screenshots/day1/Outliers_3.png)

![ IMAGE SPACE – Boxplot Example (Total Day Minutes) ](../Screenshots/day1/Outliers_4.png)

### Observations

* Mild outliers detected in:

  * Total day minutes
  * Total evening minutes
  * Customer service calls
* Most extreme values likely represent genuine high-usage customers rather than data entry errors.

Outlier handling will be approached cautiously to avoid removing legitimate business behavior.

---

## Data Pipeline Implementation

Beyond notebook analysis, a structured pipeline (`data_pipeline.py`) was created to:

* Load raw dataset
* Validate structure
* Remove duplicates
* Handle missing values
* Detect and manage outliers
* Save processed dataset
* Generate automated EDA report

### Project Structure

```
week6/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   └── pipelines/
│       └── data_pipeline.py
│
├── notebooks/
|   └── eda.ipynb

```

This ensures reproducibility and scalability for future modeling.

---