TEMP_HIGH_C = 38.0
TEMP_LOW_C = 5.0
SOIL_MOIST_CRITICAL = 15.0
SOIL_MOIST_LOW = 25.0
SOIL_MOIST_WATERLOGGED = 85.0


def evaluate_thresholds(temp_c, humidity, soil_moist):
    triggered = []

    if temp_c >= TEMP_HIGH_C:
        triggered.append("heat stress: temperature at or above threshold")
    elif temp_c <= TEMP_LOW_C:
        triggered.append("frost risk: temperature at or below threshold")

    if soil_moist <= SOIL_MOIST_CRITICAL:
        triggered.append("soil moisture critically low")
    elif soil_moist <= SOIL_MOIST_LOW:
        triggered.append("soil moisture low")
    elif soil_moist >= SOIL_MOIST_WATERLOGGED:
        triggered.append("soil waterlogged")

    return "; ".join(triggered) or None


def combine_alert(threshold_alert, device_reported_alert):
    parts = [a for a in (threshold_alert, device_reported_alert) if a]
    return "; ".join(parts) or None
