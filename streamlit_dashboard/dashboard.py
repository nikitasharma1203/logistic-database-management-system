import streamlit as st
import pandas as pd
import os
import plotly.express as px
import helper as an

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Logistics Intelligence Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (CACHED)
# -----------------------------
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_FILE = os.path.join(BASE_DIR, "data", "logistics_data.xlsx")
    df = pd.read_excel(DATA_FILE)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

origin = st.sidebar.multiselect(
    "Origin Port",
    df["origin_port"].dropna().unique(),
    default=df["origin_port"].dropna().unique()
)

service = st.sidebar.multiselect(
    "Service Level",
    df["service_level"].dropna().unique(),
    default=df["service_level"].dropna().unique()
)

carrier = st.sidebar.multiselect(
    "Carrier",
    df["carrier"].dropna().unique(),
    default=df["carrier"].dropna().unique()
)

# Apply filters
filtered_df = df[
    (df["origin_port"].isin(origin)) &
    (df["service_level"].isin(service)) &
    (df["carrier"].isin(carrier))
]

# -----------------------------
# HEADER
# -----------------------------
st.title("📦 Logistics Intelligence Dashboard")
st.caption("Operational insights • Performance • Data Quality")

# -----------------------------
# KPI (FROM helper.py)
# -----------------------------
kpi = an.kpi_metrics(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Orders", kpi["Total Orders"])
c2.metric("👥 Customers", kpi["Total Customers"])
c3.metric("🚚 Carriers", kpi["Total Carriers"])
c4.metric("⚖️ Avg Weight", round(kpi["Avg Weight"], 2))

st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🚚 Operations",
    "📈 Trends",
    "🧠 Intelligence"
])

# =============================
# TAB 1: OVERVIEW
# =============================
with tab1:
    st.subheader("Orders by Origin Port")

    origin_df = an.orders_by_origin_port(filtered_df)

    fig1 = px.bar(origin_df, x="origin_port", y="total_orders",
                  color="total_orders")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Service Level Distribution")

    svc_df = an.service_level_distribution(filtered_df)

    fig2 = px.pie(svc_df, values="count", names="service_level")
    st.plotly_chart(fig2, use_container_width=True)

# =============================
# TAB 2: OPERATIONS
# =============================
with tab2:
    st.subheader("Carrier Productivity")

    carrier_df = an.carrier_productivity(filtered_df)

    y_col = "shipments" if "shipments" in carrier_df.columns else "shipments_handled"

    fig3 = px.bar(carrier_df, x="carrier", y=y_col, color=y_col)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top Customers")

    top_customers = (
        filtered_df.groupby("customer_id")
        .size()
        .reset_index(name="orders")
        .sort_values(by="orders", ascending=False)
        .head(10)
    )

    fig4 = px.bar(top_customers, x="customer_id", y="orders")
    st.plotly_chart(fig4, use_container_width=True)

# =============================
# TAB 3: TRENDS
# =============================
with tab3:
    st.subheader("Monthly Orders Trend")

    monthly_df = an.monthly_orders(filtered_df)

    fig5 = px.line(monthly_df, x="month", y="orders", markers=True)
    st.plotly_chart(fig5, use_container_width=True)

# =============================
# TAB 4: INTELLIGENCE
# =============================
with tab4:
    st.subheader("Churn Prediction")

    churn_df = an.churn_prediction(filtered_df)

    fig6 = px.histogram(churn_df, x="status", color="status")
    st.plotly_chart(fig6, use_container_width=True)

    # 🔥 High risk customers
    if "churn_probability" in churn_df.columns:
        risky = churn_df[churn_df["churn_probability"] > 0.7]
        st.warning(f"⚠️ {len(risky)} High Risk Customers")

    st.subheader("Data Quality")

    dq_df = an.data_quality_report(filtered_df)

    fig7 = px.bar(dq_df, x=dq_df.index, y="issue_count")
    st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# DOWNLOAD
# -----------------------------
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)
