"""
Digital Triplet — FastAPI Ingestion Server
Receives live telemetry from ESP32 (/data) and MYOSA (/edge) boards,
merges them, runs anomaly detection + digital twin comparison,
and writes enriched rows to sensor_data.csv for the Streamlit dashboard.
"""

import os
import sys
import threading
from datetime import datetime

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# ── Ensure local imports work ──
sys.path.insert(0, os.path.dirname(__file__))
from anomaly_detection import AnomalyDetector
from digital_twin import DigitalTwinModel

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "sensor_data.csv")
MAX_ROWS = 100

app = FastAPI(title="Digital Triplet Ingestion Server", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Shared state
detector = AnomalyDetector()
digital_twin = DigitalTwinModel()
csv_lock = threading.Lock()

# Latest MYOSA cache (updated at ~200ms, consumed when ESP32 data arrives at ~1s)
myosa_cache = {
    "pressure": 1013.25,       # hPa — default sea-level
    "edge_vibration": 9.81,    # m/s² — default gravity only
    "color_cmd": "MONITORING", # Default command
}

# ─────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────

class ESP32Payload(BaseModel):
    rpm: float = 0.0
    temperature: float = 0.0
    vibration: float = 0.0
    current: float = 0.0
    voltage: float = 0.0
    power: float = 0.0


class MYOSAPayload(BaseModel):
    device: Optional[str] = "myosa_edge_node"
    pressure: float = 1013.25
    edge_vibration: float = 9.81
    color_cmd: str = "MONITORING"


# ─────────────────────────────────────────────
# CSV I/O (thread-safe)
# ─────────────────────────────────────────────

def load_existing_data() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        try:
            return pd.read_csv(CSV_PATH)
        except (pd.errors.EmptyDataError, pd.errors.ParserError, IOError):
            pass
    return pd.DataFrame()


def save_data(df: pd.DataFrame) -> None:
    df = df.tail(MAX_ROWS).reset_index(drop=True)
    tmp_path = CSV_PATH + ".tmp"
    df.to_csv(tmp_path, index=False)
    os.replace(tmp_path, CSV_PATH)


def append_reading(new_row: dict) -> pd.DataFrame:
    with csv_lock:
        df = load_existing_data()
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        save_data(df)
        return df


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.post("/data")
async def receive_esp32_data(payload: ESP32Payload):
    """
    Receive ESP32 motor telemetry (every ~1s).
    Merges with latest MYOSA cache, runs analysis, writes to CSV.
    """
    # Merge with MYOSA cache
    pressure = myosa_cache["pressure"]
    edge_vibration = myosa_cache["edge_vibration"]
    color_cmd = myosa_cache["color_cmd"]

    # Run anomaly detection (includes color_cmd override logic)
    analysis = detector.analyze(
        rpm=payload.rpm,
        temp=payload.temperature,
        vib=payload.vibration,
        curr=payload.current,
        pressure=pressure,
        color_cmd=color_cmd,
    )

    # Run digital twin comparison
    twin_data = digital_twin.compare(
        actual_rpm=payload.rpm,
        actual_temp=payload.temperature,
        actual_vib=payload.vibration,
        actual_curr=payload.current,
        actual_voltage=payload.voltage,
        actual_power=payload.power,
        actual_pressure=pressure,
    )

    # Build enriched row
    row = {
        "timestamp":            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # ESP32 sensors
        "rpm":                  round(payload.rpm, 2),
        "temperature":          round(payload.temperature, 2),
        "vibration":            round(payload.vibration, 3),
        "current":              round(payload.current, 3),
        "voltage":              round(payload.voltage, 2),
        "power":                round(payload.power, 2),
        # MYOSA sensors
        "pressure":             round(pressure, 2),
        "edge_vibration":       round(edge_vibration, 2),
        "color_cmd":            color_cmd,
        # Anomaly detection
        "health_score":         analysis["health_score"],
        "status":               analysis["status"],
        "anomaly_reason":       analysis["anomaly_reason"],
        "recommendation":       analysis["recommendation"],
        "ai_action":            analysis["ai_action"],
        "fault_type":           color_cmd if color_cmd != "GREEN_RUN" and color_cmd != "MONITORING" else "none",
        "fault_severity":       "Severe" if color_cmd == "RED_STOP" else ("Moderate" if color_cmd == "BLUE_MAINT" else "None"),
        # Digital twin
        "expected_rpm":         twin_data["expected_rpm"],
        "expected_temperature": twin_data["expected_temperature"],
        "expected_vibration":   twin_data["expected_vibration"],
        "expected_current":     twin_data["expected_current"],
        "expected_voltage":     twin_data["expected_voltage"],
        "expected_power":       twin_data["expected_power"],
        "expected_pressure":    twin_data["expected_pressure"],
        "deviation_score":      twin_data["deviation_score"],
        "twin_status":          twin_data["twin_status"],
    }

    df = append_reading(row)

    tag = f"[{row['status'].upper()}]".ljust(10)
    print(
        f"[{row['timestamp']}] {tag} | "
        f"RPM={row['rpm']} T={row['temperature']}°C V={row['vibration']}mm/s "
        f"I={row['current']}A V={row['voltage']}V P={row['power']}W | "
        f"MYOSA: {row['pressure']}hPa cmd={row['color_cmd']} | "
        f"Health={row['health_score']}% Dev={row['deviation_score']}%"
    )

    return {"status": "ok", "rows": len(df), "health_score": row["health_score"]}


@app.post("/edge")
async def receive_myosa_data(payload: MYOSAPayload):
    """
    Receive MYOSA edge node telemetry (every ~200ms).
    Stores in cache — merged into the next ESP32 data write.
    """
    myosa_cache["pressure"] = payload.pressure
    myosa_cache["edge_vibration"] = payload.edge_vibration
    myosa_cache["color_cmd"] = payload.color_cmd

    print(
        f"[MYOSA] Pressure={payload.pressure:.1f}hPa "
        f"EdgeVib={payload.edge_vibration:.2f} "
        f"Cmd={payload.color_cmd}"
    )
    return {"status": "ok", "cached": True}


class TrinityQuery(BaseModel):
    query: str
    telemetry: dict


@app.post("/ask-trinity")
async def ask_trinity(payload: TrinityQuery):
    """
    Local industrial AI mock endpoint.
    Parses the user query and the current telemetry state to respond like an AI.
    """
    query = payload.query.lower()
    t = payload.telemetry
    
    # Default fallback
    response = "I am monitoring the systems. No immediate action required."
    proof_type = "none"
    proof_value = 0.0

    health = t.get("health_score", 100)
    rpm = t.get("rpm", 0)
    temp = t.get("temperature", 25.0)
    vib = t.get("vibration", 0.0)
    status = t.get("status", "normal")
    cmd = t.get("color_cmd", "MONITORING")

    # Intent routing based on keywords
    if "health" in query or "status" in query or "how is" in query:
        if status == "critical":
            response = f"System health is critical at {health}%. Immediate intervention recommended."
        elif status == "warning":
            response = f"System health is at {health}%. Performance degradation detected."
        else:
            response = f"Motor health remains stable at {health}%. No anomalies detected."
        proof_type = "health"
        proof_value = float(health)

    elif "temperature" in query or "hot" in query or "temp" in query:
        if temp > 75:
            response = f"Thermal threshold exceeded. Core temperature is critically high at {temp} degrees Celsius."
        elif temp > 60:
            response = f"Temperature elevated to {temp} degrees. Engaging thermal buffer monitoring."
        else:
            response = f"Thermal levels nominal. Core running at {temp} degrees Celsius."
        proof_type = "temperature"
        proof_value = float(temp)

    elif "vibration" in query or "shake" in query or "unstable" in query:
        if vib > 15:
            response = f"Severe structural vibration detected at {vib} millimeters per second. Bearing failure imminent."
        elif vib > 8:
            response = f"Abnormal harmonic vibration at {vib} millimeters per second. Check rotor alignment."
        else:
            response = f"Vibration signatures are within operational tolerances at {vib} millimeters per second."
        proof_type = "vibration"
        proof_value = float(vib)

    elif "rpm" in query or "speed" in query or "fast" in query:
        response = f"Current rotation speed is {rpm} RPM. Operational phase locked."
        proof_type = "rpm"
        proof_value = float(rpm)

    elif "stop" in query or "halt" in query or "red" in query:
        response = "Emergency stop sequence acknowledged. Decelerating motor."
        proof_type = "anomaly"
        proof_value = 99.9

    elif "run" in query or "start" in query or "green" in query:
        response = "Run sequence initiated. Bringing systems online."
        proof_type = "health"
        proof_value = 100.0
        
    elif "anomaly" in query or "problem" in query or "issue" in query:
        if status != "normal":
            response = f"Anomaly detected. Signature matches {t.get('anomaly_reason', 'unknown interference')}."
            proof_type = "anomaly"
            proof_value = 85.5
        else:
            response = "No distinct anomaly signatures found in the current telemetry stream."
            proof_type = "none"
            proof_value = 0.0

    return {
        "response": response,
        "proof_type": proof_type,
        "proof_value": proof_value
    }


@app.get("/health")
async def health_check():
    """Simple health-check endpoint."""
    return {
        "status": "online",
        "myosa_cache": myosa_cache,
        "csv_path": CSV_PATH,
    }


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 80)
    print("  Digital Triplet — Ingestion Server")
    print(f"  Listening on http://0.0.0.0:8000")
    print(f"  ESP32  endpoint : POST /data")
    print(f"  MYOSA  endpoint : POST /edge")
    print(f"  CSV output      : {CSV_PATH}")
    print("=" * 80)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
