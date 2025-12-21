import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
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

fig, ax = plt.subplots()
ax.bar(origin_df["origin_port"], origin_df["total_orders"], color="skyblue")
ax.set_title("Orders by Origin Port")
ax.set_xlabel("Origin Port")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# Monthly Orders Trend
st.subheader("Monthly Orders Trend")
monthly_df = an.monthly_orders(df)
st.dataframe(monthly_df)

fig, ax = plt.subplots()
ax.plot(monthly_df["month"], monthly_df["orders"], marker="o", color="green")
ax.set_title("Monthly Orders Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# Service Level Distribution
st.subheader("Service Level Distribution")
svc_df = an.service_level_distribution(df)
st.dataframe(svc_df)

fig, ax = plt.subplots()
ax.pie(svc_df["count"], labels=svc_df["service_level"], autopct="%1.1f%%")
ax.set_title("Service Level Distribution")
st.pyplot(fig)

# Carrier Productivity
st.subheader("Carrier Productivity")
carrier_df = an.carrier_productivity(df)
st.dataframe(carrier_df)

fig, ax = plt.subplots()
ax.bar(carrier_df["carrier"], carrier_df["shipments"], color="orange")
ax.set_title("Carrier Productivity")
ax.set_xlabel("Carrier")
ax.set_ylabel("Shipments")
plt.xticks(rotation=45)
st.pyplot(fig)

# Churn Prediction
st.subheader("Churn Prediction")
churn_df = an.churn_prediction(df)
st.dataframe(churn_df)

# Data Quality Report
st.subheader("Data Quality Report")
dq_df = an.data_quality_report(df)
st.dataframe(dq_df)
