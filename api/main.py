from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from api.auth import verify_device
from api.db import init_db, insert_reading, fetch_readings, get_device

app = FastAPI(title="Terrin Ingestion API")


@app.on_event("startup")
def startup():
    init_db()


class Reading(BaseModel):
    device_id: str
    temp_c: float
    humidity: float = Field(ge=0, le=100)
    soil_moist: float = Field(ge=0, le=100)
    alert: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/readings", status_code=201)
def create_reading(reading: Reading, x_device_key: Optional[str] = Header(None)):
    if not verify_device(reading.device_id, x_device_key):
        raise HTTPException(status_code=401, detail="invalid device key")
    device = get_device(reading.device_id)
    reading_id = insert_reading(
        reading.device_id,
        device["farm_id"],
        reading.temp_c,
        reading.humidity,
        reading.soil_moist,
        reading.alert,
    )
    return {"id": reading_id}


@app.get("/v1/readings")
def list_readings(
    farm_id: Optional[str] = None,
    device_id: Optional[str] = None,
    limit: int = 100,
):
    return fetch_readings(farm_id=farm_id, device_id=device_id, limit=min(limit, 500))
