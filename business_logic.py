from typing import Dict

def calculate_incident_metrics(data: Dict):

    picked = data["employees_picked"]
    waiting = data["employees_waiting"]
    backup = data["backup_capacity"]
    weather = data["weather"]
    breakdown = data["vehicle_breakdown"]
    driver = data["driver_absent"]

    affected = picked + waiting
    shortage = max(0, waiting - backup)

    risk_score = 0

    if driver.strip():
        risk_score += 35

    if breakdown.strip():
        risk_score += 30

    if weather == "Rain":
        risk_score += 10

    elif weather == "Heavy Rain":
        risk_score += 20

    risk_score += waiting * 5
    risk_score += shortage * 10

    if risk_score >= 80:
        priority = "Critical"
    elif risk_score >= 60:
        priority = "High"
    elif risk_score >= 35:
        priority = "Medium"
    else:
        priority = "Low"

    if shortage == 0:
        delay = "10-15 mins"
    elif shortage <= 2:
        delay = "20-30 mins"
    else:
        delay = "30+ mins"

    return {
        "affected_employees": affected,
        "capacity_shortage": shortage,
        "priority": priority,
        "risk_score": risk_score,
        "estimated_delay": delay
    }