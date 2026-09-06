import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("TERRIN_DB_PATH", "data/db/terrin.db")

READINGS_SCHEMA = """CREATE TABLE IF NOT EXISTS readings (
  id INTEGER PRIMARY KEY,
  device_id TEXT NOT NULL,
  farm_id TEXT NOT NULL,
  temp_c REAL,
  humidity REAL,
  soil_moist REAL,
  alert TEXT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
)"""

DEVICES_SCHEMA = """CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY,
  farm_id TEXT NOT NULL,
  api_key_hash TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)"""


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute(READINGS_SCHEMA)
        con.execute(DEVICES_SCHEMA)


@contextmanager
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


def insert_reading(device_id, farm_id, temp_c, humidity, soil_moist, alert):
    with get_db() as con:
        cur = con.execute(
            "INSERT INTO readings (device_id, farm_id, temp_c, humidity, soil_moist, alert) "
            "VALUES (?,?,?,?,?,?)",
            (device_id, farm_id, temp_c, humidity, soil_moist, alert),
        )
        con.commit()
        return cur.lastrowid


def register_device(device_id, farm_id, api_key_hash):
    with get_db() as con:
        con.execute(
            "INSERT INTO devices (device_id, farm_id, api_key_hash) VALUES (?,?,?) "
            "ON CONFLICT(device_id) DO UPDATE SET farm_id=excluded.farm_id, api_key_hash=excluded.api_key_hash",
            (device_id, farm_id, api_key_hash),
        )
        con.commit()


def get_device(device_id):
    with get_db() as con:
        row = con.execute(
            "SELECT * FROM devices WHERE device_id = ?", (device_id,)
        ).fetchone()
        return dict(row) if row else None


def fetch_readings(farm_id=None, device_id=None, limit=100):
    clauses, params = [], []
    if farm_id:
        clauses.append("farm_id = ?")
        params.append(farm_id)
    if device_id:
        clauses.append("device_id = ?")
        params.append(device_id)
    query = "SELECT * FROM readings"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    with get_db() as con:
        return [dict(row) for row in con.execute(query, params).fetchall()]
