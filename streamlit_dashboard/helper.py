import pandas as pd

# -------------------------------
# 1. Orders by Origin Port
# -------------------------------
def orders_by_origin_port(orders: pd.DataFrame) -> pd.DataFrame:
    df = (
        orders
        .groupby("origin_port")
        .agg(
            total_orders=("order_id", "count"),
            avg_weight=("weight", "mean")
        )
        .reset_index()
        .sort_values(by="total_orders", ascending=False)
    )
    df["avg_weight"] = df["avg_weight"].round(2)
    return df


# -------------------------------
# 2. Domestic vs International
# -------------------------------
def geographic_distribution(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    orders["shipment_type"] = orders.apply(
        lambda x: "Domestic"
        if x["origin_port"] == x["destination_port"]
        else "International",
        axis=1
    )

    return (
        orders
        .groupby("shipment_type")
        .agg(
            total_orders=("order_id", "count"),
            avg_weight=("weight", "mean")
        )
        .reset_index()
    )


# -------------------------------
# 3. Failed Deliveries by Branch
# -------------------------------
def failed_deliveries_by_branch(orders: pd.DataFrame) -> pd.DataFrame:
    return (
        orders[orders["ship_late_day_count"] > 0]
        .groupby("plant_code")
        .size()
        .reset_index(name="failed_orders")
        .sort_values(by="failed_orders", ascending=False)
    )


# -------------------------------
# 4. Shipment Weight Outliers
# -------------------------------
def shipment_weight_outliers(orders: pd.DataFrame) -> pd.DataFrame:
    mean_wt = orders["weight"].mean()
    std_wt = orders["weight"].std()
    return orders[orders["weight"] > mean_wt + 2 * std_wt]


# -------------------------------
# 5. Customer Shipment Summary
# -------------------------------
def customer_summary(orders: pd.DataFrame) -> pd.DataFrame:
    return (
        orders
        .groupby("customer")
        .agg(
            shipment_count=("order_id", "count"),
            total_quantity=("unit_quantity", "sum"),
            late_shipments=("ship_late_day_count", lambda x: (x > 0).sum())
        )
        .reset_index()
    )


# -------------------------------
# 6. Customer Segmentation
# -------------------------------
def customer_segmentation(customer_df: pd.DataFrame) -> pd.DataFrame:
    def segment(cnt):
        if cnt > 100:
            return "VIP"
        elif cnt > 50:
            return "Premium"
        elif cnt > 10:
            return "Regular"
        else:
            return "New"

    customer_df = customer_df.copy()
    customer_df["segment"] = customer_df["shipment_count"].apply(segment)
    return customer_df


# -------------------------------
# 7. Churn Prediction
# -------------------------------
def churn_prediction(orders: pd.DataFrame) -> pd.DataFrame:
    last_activity = (
        orders
        .groupby("customer")["order_date"]
        .max()
        .reset_index()
    )

    latest_date = orders["order_date"].max()
    last_activity["days_inactive"] = (
        latest_date - last_activity["order_date"]
    ).dt.days

    last_activity["status"] = last_activity["days_inactive"].apply(
        lambda x: "Active" if x < 30 else "At Risk" if x < 90 else "Legacy"
    )

    return last_activity


# -------------------------------
# 8. Carrier Productivity
# -------------------------------
def carrier_productivity(orders: pd.DataFrame) -> pd.DataFrame:
    df = (
        orders
        .groupby("carrier")
        .agg(
            shipments_handled=("order_id", "count"),
            avg_weight=("weight", "mean"),
            late_shipments=("ship_late_day_count", lambda x: (x > 0).sum())
        )
        .reset_index()
    )

    df["success_rate"] = (
        1 - df["late_shipments"] / df["shipments_handled"]
    )

    return df.sort_values(by="success_rate", ascending=False)


# -------------------------------
# 9. Data Quality Checks
# -------------------------------
def data_quality_report(orders: pd.DataFrame) -> pd.DataFrame:
    issues = {
        "missing_origin_port": orders["origin_port"].isnull().sum(),
        "missing_destination_port": orders["destination_port"].isnull().sum(),
        "missing_customer": orders["customer"].isnull().sum(),
        "invalid_weight": (orders["weight"] <= 0).sum()
    }
    return pd.DataFrame.from_dict(issues, orient="index", columns=["issue_count"])


# -------------------------
# KPI Metrics
# -------------------------
def kpi_metrics(df):
    return {
        "Total Orders": len(df),
        "Total Customers": df["customer"].nunique(),
        "Total Carriers": df["carrier"].nunique(),
        "Avg Weight": round(df["weight"].mean(), 2)
    }


# -------------------------
# Service Level Distribution
# -------------------------
def service_level_distribution(df):
    return df.groupby("service_level").size().reset_index(name="count")


# -------------------------
# Time Series Trend
# -------------------------
def monthly_orders(df):
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df.groupby("month")["order_id"].count().reset_index(name="orders")


def daily_orders(df):
    return (
        df.groupby(df["order_date"].dt.date)
        .size()
        .reset_index(name="orders")
        .rename(columns={"order_date": "date"})
    )
