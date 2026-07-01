import sqlite3, time
from rover.sensors import read

DB = "data/db/terrin.db"

def init():
  con = sqlite3.connect(DB)
  con.execute("""CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY,
    device_id TEXT, farm_id TEXT,
    temp_c REAL, humidity REAL,
    soil_moist REAL, alert TEXT,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP)""")
  con.commit(); con.close()

def log():
  while True:
    r = read()
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO readings VALUES (NULL,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
      ("dev-001","farm-001",r["temp_c"],r["humidity"],r["soil_moist"],r["alert"]))
    con.commit(); con.close()
    time.sleep(1800)