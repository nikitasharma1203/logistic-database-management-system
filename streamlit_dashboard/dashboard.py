import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import helper as an   

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM supply_chain.orders", engine)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

orders = load_data()

st.title("📦 Supply Chain Analytics Dashboard")

option = st.sidebar.selectbox("Select Analysis",["Origin Port Summary","Geographic Distribution","Failed Deliveries","Customer Segmentation","Carrier Productivity","Data Quality"])

if option == "Origin Port Summary":
    st.subheader("Orders by Origin Port")
    st.dataframe(an.orders_by_origin_port(orders))

elif option == "Geographic Distribution":
    st.subheader("Domestic vs International")
    st.dataframe(an.geographic_distribution(orders))

elif option == "Failed Deliveries":
    st.subheader("Branches with Failed Deliveries")
    st.dataframe(an.failed_deliveries_by_branch(orders))

elif option == "Customer Segmentation":
    st.subheader("Customer Segments")
    cust = an.customer_summary(orders)
    st.dataframe(an.customer_segmentation(cust))

elif option == "Carrier Productivity":
    st.subheader("Carrier Productivity Ranking")
    st.dataframe(an.carrier_productivity(orders))

elif option == "Data Quality":
    st.subheader("Data Quality Report")
    st.dataframe(an.data_quality_report(orders))
kpis = an.kpi_metrics(orders)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total Orders", kpis["Total Orders"])
c2.metric("👥 Customers", kpis["Total Customers"])
c3.metric("🚚 Carriers", kpis["Total Carriers"])
c4.metric("⚖ Avg Weight", kpis["Avg Weight"])
st.subheader("Orders by Origin Port")
origin_df = an.orders_by_origin_port(orders)
st.bar_chart(origin_df.set_index("origin_port")["total_orders"])
st.subheader("Service Level Distribution")
svc = an.service_level_distribution(orders)
st.pyplot(
    svc.set_index("service_level")
       .plot.pie(y="count", autopct="%1.1f%%", figsize=(6,6))
       .figure
)

st.subheader("Carrier Productivity Ranking")
st.dataframe(an.carrier_productivity(orders))

st.subheader("Monthly Shipment Summary")

monthly = an.monthly_orders(orders)

st.metric(
    label="Shipments in May 2013",
    value=int(monthly["orders"].iloc[0])
)

st.subheader("Shipment Snapshot – May 26, 2013")

st.metric("Total Shipments", len(orders))
st.metric("Unique Customers", orders["customer"].nunique())
st.metric("Active Carriers", orders["carrier"].nunique())
st.subheader("Shipments by Carrier")

carrier_dist = orders["carrier"].value_counts().head(10)
st.bar_chart(carrier_dist)
st.subheader("Shipment Weight Distribution")

st.bar_chart(
    orders["weight"]
    .round()
    .value_counts()
    .sort_index()
)
