import streamlit as st
import pandas as pd
import os
import plotly.express as px
import helper as an

# -----------------------------
# Load data from Excel
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "logistics_data.xlsx")

df = pd.read_excel(DATA_FILE)

# Normalize column names: lowercase, strip spaces, replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -----------------------------
# Streamlit Dashboard
# -----------------------------
st.title("📦 Logistics Dashboard")

# KPI Metrics
st.subheader("Key Performance Indicators")
kpi = an.kpi_metrics(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", kpi["Total Orders"])
col2.metric("Total Customers", kpi["Total Customers"])
col3.metric("Total Carriers", kpi["Total Carriers"])
col4.metric("Avg Weight", kpi["Avg Weight"])

# Orders by Origin Port
st.subheader("Orders by Origin Port")
origin_df = an.orders_by_origin_port(df)
st.dataframe(origin_df)

fig_origin = px.bar(origin_df, x="origin_port", y="total_orders",
                    title="Orders by Origin Port",
                    labels={"origin_port": "Origin Port", "total_orders": "Total Orders"},
                    color="total_orders")
st.plotly_chart(fig_origin, use_container_width=True)

# Monthly Orders Trend
st.subheader("Monthly Orders Trend")
monthly_df = an.monthly_orders(df)
st.dataframe(monthly_df)

fig_monthly = px.line(monthly_df, x="month", y="orders",
                      title="Monthly Orders Trend",
                      markers=True)
st.plotly_chart(fig_monthly, use_container_width=True)

# Service Level Distribution
st.subheader("Service Level Distribution")
svc_df = an.service_level_distribution(df)
st.dataframe(svc_df)

fig_service = px.pie(svc_df, values="count", names="service_level",
                     title="Service Level Distribution")
st.plotly_chart(fig_service, use_container_width=True)

# Carrier Productivity
st.subheader("Carrier Productivity")
carrier_df = an.carrier_productivity(df)
st.dataframe(carrier_df)

# ✅ Fix: use the correct column name from helper.py
y_col = "shipments" if "shipments" in carrier_df.columns else "shipments_handled"

fig_carrier = px.bar(carrier_df, x="carrier", y=y_col,
                     title="Carrier Productivity",
                     labels={"carrier": "Carrier", y_col: "Shipments"},
                     color=y_col)
st.plotly_chart(fig_carrier, use_container_width=True)

# Churn Prediction
st.subheader("Churn Prediction")
churn_df = an.churn_prediction(df)
st.dataframe(churn_df)

fig_churn = px.histogram(churn_df, x="status", color="status",
                         title="Customer Status Distribution")
st.plotly_chart(fig_churn, use_container_width=True)

# Data Quality Report
st.subheader("Data Quality Report")
dq_df = an.data_quality_report(df)
st.dataframe(dq_df)

fig_dq = px.bar(dq_df, x=dq_df.index, y="issue_count",
                title="Data Quality Issues",
                labels={"issue_count": "Issue Count"})
st.plotly_chart(fig_dq, use_container_width=True)
