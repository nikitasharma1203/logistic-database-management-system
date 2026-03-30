import streamlit as st
import pandas as pd
import os
import plotly.express as px
import helper as an

st.set_page_config(page_title="Logistics Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (SAFE)
# -----------------------------
@st.cache_data
def load_data():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_FILE = os.path.join(BASE_DIR, "data", "logistics_data.xlsx")

        df = pd.read_excel(DATA_FILE)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        return df

    except Exception as e:
        st.error(f"❌ Data Load Error: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

def safe_filter(df, col):
    return df[col].dropna().unique() if col in df else []

origin = st.sidebar.multiselect("Origin Port", safe_filter(df, "origin_port"), default=safe_filter(df, "origin_port"))
service = st.sidebar.multiselect("Service Level", safe_filter(df, "service_level"), default=safe_filter(df, "service_level"))
carrier = st.sidebar.multiselect("Carrier", safe_filter(df, "carrier"), default=safe_filter(df, "carrier"))

filtered_df = df[
    (df["origin_port"].isin(origin)) &
    (df["service_level"].isin(service)) &
    (df["carrier"].isin(carrier))
]

# -----------------------------
# HEADER
# -----------------------------
st.title("📦 Logistics Intelligence Dashboard")

# -----------------------------
# KPI
# -----------------------------
kpi = an.kpi_metrics(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders", kpi["Total Orders"])
c2.metric("Customers", kpi["Total Customers"])
c3.metric("Carriers", kpi["Total Carriers"])
c4.metric("Avg Weight", round(kpi["Avg Weight"], 2))

st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Operations", "Trends", "Intelligence"])

# OVERVIEW
with tab1:
    origin_df = an.orders_by_origin_port(filtered_df)
    st.plotly_chart(px.bar(origin_df, x="origin_port", y="total_orders"))

    svc_df = an.service_level_distribution(filtered_df)
    st.plotly_chart(px.pie(svc_df, names="service_level", values="count"))

# OPERATIONS
with tab2:
    carrier_df = an.carrier_productivity(filtered_df)
    st.plotly_chart(px.bar(carrier_df, x="carrier", y="shipments"))

# TRENDS
with tab3:
    monthly_df = an.monthly_orders(filtered_df)
    st.plotly_chart(px.line(monthly_df, x="month", y="orders"))

# INTELLIGENCE
with tab4:
    churn_df = an.churn_prediction(filtered_df)
    st.dataframe(churn_df)

    delay_df = an.delay_analysis(filtered_df)
    st.plotly_chart(px.bar(delay_df, x="origin_port", y="delays"))

    seg_df = an.customer_segmentation(filtered_df)
    st.plotly_chart(px.histogram(seg_df, x="segment"))

# DOWNLOAD
st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "data.csv"
)
