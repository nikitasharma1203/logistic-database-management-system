# ==============================
# 🚀 HELPER.PY (Cloud-Proof Analytics + ML)
# ==============================

import pandas as pd
import numpy as np

# -----------------------------
# SAFE ML IMPORT
# -----------------------------
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except:
    SKLEARN_AVAILABLE = False

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
    if "origin_port" not in df:
        return pd.DataFrame({"origin_port": [], "total_orders": []})
    return df.groupby("origin_port").size().reset_index(name="total_orders")

# -----------------------------
# MONTHLY ORDERS (SAFE)
# -----------------------------
def monthly_orders(df):
    if "order_date" not in df:
        return pd.DataFrame({"month": [], "orders": []})

    df = df.copy()

    try:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        df = df.dropna(subset=["order_date"])
        df["month"] = df["order_date"].dt.to_period("M").astype(str)

        return df.groupby("month").size().reset_index(name="orders")

    except:
        return pd.DataFrame({"month": [], "orders": []})

# -----------------------------
# SERVICE LEVEL DISTRIBUTION
# -----------------------------
def service_level_distribution(df):
    if "service_level" not in df:
        return pd.DataFrame({"service_level": [], "count": []})

    return df["service_level"].value_counts().reset_index().rename(
        columns={"index": "service_level", "service_level": "count"}
    )

# -----------------------------
# CARRIER PRODUCTIVITY
# -----------------------------
def carrier_productivity(df):
    if "carrier" not in df:
        return pd.DataFrame({"carrier": [], "shipments": []})

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
# ML: CHURN PREDICTION (SAFE)
# =============================
def churn_prediction(df):
    if not SKLEARN_AVAILABLE:
        return pd.DataFrame({
            "status": ["⚠️ sklearn not installed - ML disabled"]
        })

    df = df.copy()

    required_cols = ["service_level", "carrier"]
    if not all(col in df.columns for col in required_cols):
        return pd.DataFrame({
            "status": ["⚠️ Not enough features for ML"]
        })

    try:
        if "churn" not in df:
            df["churn"] = np.random.randint(0, 2, len(df))

        X = df[required_cols].copy()
        y = df["churn"]

        for col in X.columns:
            X[col] = LabelEncoder().fit_transform(X[col].astype(str))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        probs = model.predict_proba(X)[:, 1]

        result = pd.DataFrame()
        result["churn_probability"] = probs
        result["status"] = np.where(probs > 0.5, "Likely to Churn", "Safe")

        return result

    except Exception as e:
        return pd.DataFrame({
            "status": [f"⚠️ ML Error: {str(e)}"]
        })

# =============================
# DELAY ANALYSIS
# =============================
def delay_analysis(df):
    if "delivery_time" not in df:
        return pd.DataFrame({"origin_port": [], "delays": []})

    avg_time = df["delivery_time"].mean()
    delayed = df[df["delivery_time"] > avg_time]

    return delayed.groupby("origin_port").size().reset_index(name="delays")

# =============================
# CUSTOMER SEGMENTATION
# =============================
def customer_segmentation(df):
    if "customer_id" not in df:
        return pd.DataFrame({"customer_id": [], "segment": []})

    freq = df.groupby("customer_id").size().reset_index(name="orders")

    conditions = [
        freq["orders"] > 20,
        freq["orders"].between(10, 20),
        freq["orders"] < 10
    ]

    choices = ["High Value", "Medium Value", "Low Value"]

    freq["segment"] = np.select(conditions, choices, default="Low Value")

    return freq
