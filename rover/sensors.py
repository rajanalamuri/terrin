import random

def read():
  return {
    "temp_c": round(random.uniform(24, 38), 1),
    "humidity": round(random.uniform(55, 85), 1),
    "soil_moist": round(random.uniform(20, 70), 1),
    "device_alert": None
  }