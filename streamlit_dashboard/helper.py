# ==============================
# 🚀 HELPER.PY (Analytics + ML Engine)
# ==============================

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# -----------------------------
# KPI METRICS
# -----------------------------
def kpi_metrics(df):
    return {
        "Total Orders": len(df),
        "Total Customers": df["customer_id"].nunique() if "customer_id" in df else 0,
        "Total Carriers": df["carrier"].nunique() if "carrier" in df else 0,
        "Avg Weight": df["weight"].mean() if "weight" in df else 0
    }

# -----------------------------
# ORDERS BY ORIGIN PORT
# -----------------------------
def orders_by_origin_port(df):
    return df.groupby("origin_port").size().reset_index(name="total_orders")

# -----------------------------
# MONTHLY ORDERS
# -----------------------------
def monthly_orders(df):
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df.groupby("month").size().reset_index(name="orders")

# -----------------------------
# SERVICE LEVEL DISTRIBUTION
# -----------------------------
def service_level_distribution(df):
    return df["service_level"].value_counts().reset_index().rename(
        columns={"index": "service_level", "service_level": "count"}
    )

# -----------------------------
# CARRIER PRODUCTIVITY
# -----------------------------
def carrier_productivity(df):
    return df.groupby("carrier").size().reset_index(name="shipments")

# -----------------------------
# DATA QUALITY REPORT
# -----------------------------
def data_quality_report(df):
    report = {}
    
    report["missing_values"] = df.isnull().sum().sum()
    report["duplicate_rows"] = df.duplicated().sum()
    
    if "weight" in df:
        report["negative_weight"] = (df["weight"] < 0).sum()
    
    return pd.DataFrame.from_dict(report, orient="index", columns=["issue_count"])

# =============================
# 🔥 ML SECTION: CHURN PREDICTION
# =============================
def churn_prediction(df):
    df = df.copy()

    # Create synthetic churn label if not present
    if "churn" not in df.columns:
        df["churn"] = np.where(df["order_id"] % 5 == 0, 1, 0)

    # Select features
    features = ["service_level", "carrier"]
    features = [f for f in features if f in df.columns]

    if len(features) == 0:
        return pd.DataFrame({"status": ["No features available"]})

    X = df[features].copy()
    y = df["churn"]

    # Encode categorical
    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    # Train model
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        probs = model.predict_proba(X)[:, 1]

        result = df[["customer_id"]].copy() if "customer_id" in df else pd.DataFrame()
        result["churn_probability"] = probs
        result["status"] = np.where(probs > 0.5, "Likely to Churn", "Safe")

        return result

    except Exception as e:
        return pd.DataFrame({"status": [f"Model Error: {str(e)}"]})


# =============================
# 🔥 ADVANCED: DELAY ANALYSIS
# =============================
def delay_analysis(df):
    if "delivery_time" not in df:
        return pd.DataFrame()

    avg_time = df["delivery_time"].mean()
    delayed = df[df["delivery_time"] > avg_time]

    return delayed.groupby("origin_port").size().reset_index(name="delays")


# =============================
# 🔥 CUSTOMER SEGMENTATION
# =============================
def customer_segmentation(df):
    if "customer_id" not in df:
        return pd.DataFrame()

    freq = df.groupby("customer_id").size().reset_index(name="orders")

    conditions = [
        freq["orders"] > 20,
        freq["orders"].between(10, 20),
        freq["orders"] < 10
    ]

    choices = ["High Value", "Medium Value", "Low Value"]

    freq["segment"] = np.select(conditions, choices, default="Low Value")

    return freq
