import streamlit as st
import pandas as pd
import os
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

st.subheader("Orders by Origin Port")
st.dataframe(an.orders_by_origin_port(df))

st.subheader("Monthly Orders")
st.dataframe(an.monthly_orders(df))

st.subheader("Churn Prediction")
st.dataframe(an.churn_prediction(df))

st.subheader("Carrier Productivity")
st.dataframe(an.carrier_productivity(df))

st.subheader("Data Quality Report")
st.dataframe(an.data_quality_report(df))
