from fastapi import FastAPI
from helpers import (
    load_data,
    save_to_db,
    get_origin_summary,
    get_shipment_type,
    get_failed_deliveries,
    get_carrier_performance
)

app = FastAPI()

# Load data once
data = load_data()
orders = data["orders"]


@app.get("/")
def home():
    return {"message": "Supply Chain API Running"}


@app.post("/load-data")
def load_data_to_db():
    save_to_db(data)
    return {"status": "Data loaded to database"}


@app.get("/origin-summary")
def origin_summary():
    return get_origin_summary(orders).to_dict(orient="records")


@app.get("/shipment-type")
def shipment_type():
    return get_shipment_type(orders).to_dict(orient="records")


@app.get("/failed-deliveries")
def failed_deliveries():
    return get_failed_deliveries(orders).to_dict(orient="records")


@app.get("/carrier-performance")
def carrier_performance():
    return get_carrier_performance(orders).to_dict(orient="records")
