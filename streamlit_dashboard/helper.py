import os
import pandas as pd
from sqlalchemy import create_engine

# ---------- ENV CONFIG ----------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

EXCEL_PATH = os.getenv("EXCEL_PATH", "data/supply_chain.xlsx")
SCHEMA = "supply_chain"


# ---------- DB CONNECTION ----------
def get_engine():
    conn = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn)


# ---------- CLEANING ----------
def clean_columns(df):
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("/", "_")
        .str.replace("-", "_")
    )
    return df


# ---------- LOAD DATA ----------
def load_data():
    xls = pd.ExcelFile(EXCEL_PATH)

    orders = clean_columns(pd.read_excel(xls, "OrderList"))
    freight = clean_columns(pd.read_excel(xls, "FreightRates"))
    wh_costs = clean_columns(pd.read_excel(xls, "WhCosts"))
    plant_ports = clean_columns(pd.read_excel(xls, "PlantPorts"))
    vmi = clean_columns(pd.read_excel(xls, "VmiCustomers"))

    return {
        "orders": orders,
        "freight": freight,
        "wh_costs": wh_costs,
        "plant_ports": plant_ports,
        "vmi": vmi,
    }


# ---------- SAVE TO DB ----------
def save_to_db(data):
    engine = get_engine()

    data["orders"].to_sql("orders", engine, schema=SCHEMA, if_exists="replace", index=False)
    data["freight"].to_sql("freight_rates", engine, schema=SCHEMA, if_exists="replace", index=False)
    data["wh_costs"].to_sql("warehouse_costs", engine, schema=SCHEMA, if_exists="replace", index=False)
    data["plant_ports"].to_sql("plant_ports", engine, schema=SCHEMA, if_exists="replace", index=False)
    data["vmi"].to_sql("vmi_customers", engine, schema=SCHEMA, if_exists="replace", index=False)


# ---------- ANALYTICS ----------
def get_origin_summary(orders):
    df = (
        orders.groupby("origin_port")
        .agg(total_orders=("order_id", "count"),
             avg_weight=("weight", "mean"))
        .reset_index()
        .sort_values(by="total_orders", ascending=False)
    )
    df["avg_weight"] = df["avg_weight"].round(2)
    return df


def get_shipment_type(orders):
    orders = orders.copy()

    orders["shipment_type"] = orders.apply(
        lambda x: "Domestic" if x["origin_port"] == x["destination_port"] else "International",
        axis=1
    )

    return (
        orders.groupby("shipment_type")
        .agg(total_orders=("order_id", "count"),
             avg_weight=("weight", "mean"))
        .reset_index()
    )


def get_failed_deliveries(orders):
    return (
        orders[orders["ship_late_day_count"] > 0]
        .groupby("plant_code")
        .size()
        .reset_index(name="failed_orders")
        .sort_values(by="failed_orders", ascending=False)
    )


def get_carrier_performance(orders):
    df = (
        orders.groupby("carrier")
        .agg(
            shipments_handled=("order_id", "count"),
            avg_weight=("weight", "mean"),
            late_shipments=("ship_late_day_count", lambda x: (x > 0).sum())
        )
        .reset_index()
    )

    df["success_rate"] = 1 - (df["late_shipments"] / df["shipments_handled"])
    return df.sort_values(by="success_rate", ascending=False)
