import os
import time

import requests

from rover.sensors import read

API_URL = os.environ.get("TERRIN_API_URL", "http://localhost:8000")
DEVICE_API_KEY = os.environ.get("DEVICE_API_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID", "dev-001")
FARM_ID = os.environ.get("FARM_ID", "farm-001")
INTERVAL_SECONDS = 1800


def send(reading):
    payload = {"device_id": DEVICE_ID, "farm_id": FARM_ID, **reading}
    headers = {"X-Device-Key": DEVICE_API_KEY} if DEVICE_API_KEY else {}
    resp = requests.post(f"{API_URL}/v1/readings", json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def run():
    while True:
        try:
            send(read())
        except requests.RequestException as exc:
            print(f"failed to send reading: {exc}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
