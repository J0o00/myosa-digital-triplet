"""
Electric Motor Digital Triplet - Telemetry Generator
Simulates real-time sensor data, including persistent fault injection 
and autonomous AI safe mode mitigation.
"""

import pandas as pd
import random
import time
from datetime import datetime
import os
from anomaly_detection import AnomalyDetector
from digital_twin import DigitalTwinModel

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "sensor_data.csv")
MAX_ROWS = 100
INTERVAL_SECONDS = 1

NORMAL_RANGES = {
    "rpm":         (1400, 1600),
    "temperature": (55.0, 75.0),
    "vibration":   (0.5, 2.5),
    "current":     (8.0, 12.0),
}

# ─────────────────────────────────────────────
# Fault Injector System
# ─────────────────────────────────────────────

class FaultInjector:
    def __init__(self):
        self.active_fault = "none"
        self.fault_ticks = 0
        self.fault_duration = 0
        self.fault_types = ["bearing_imbalance", "thermal_overload", "current_surge", "rpm_instability"]
        
    def tick(self):
        if self.active_fault == "none":
            if random.random() < 0.04:  # 4% chance per second to start a fault (~every 25s)
                self.active_fault = random.choice(self.fault_types)
                self.fault_ticks = 0
                self.fault_duration = random.randint(15, 25)
        else:
            self.fault_ticks += 1
            if self.fault_ticks >= self.fault_duration:
                self.active_fault = "none"
                self.fault_ticks = 0
                
    def apply_fault(self, rpm, temp, vib, curr, safe_mode):
        """Applies persistent drift to simulate progressive hardware failure."""
        if self.active_fault == "none":
            return rpm, temp, vib, curr, "None"
            
        progress = self.fault_ticks / self.fault_duration
        
        # Calculate severity based on progression
        if progress < 0.3:
            severity = "Low"
            mult = 0.5
        elif progress < 0.7:
            severity = "Moderate"
            mult = 1.0
        else:
            severity = "Severe"
            mult = 1.5
            
        # Apply fault profile (if safe mode is on, faults still apply but from a lower baseline)
        if self.active_fault == "bearing_imbalance":
            vib += 1.5 + (3.0 * mult)
        elif self.active_fault == "thermal_overload":
            temp += 5.0 + (30.0 * progress)
        elif self.active_fault == "current_surge":
            curr += 3.0 + (12.0 * random.random() * mult)
        elif self.active_fault == "rpm_instability":
            rpm += random.uniform(-150 * mult, 150 * mult)
            
        return rpm, temp, vib, curr, severity

# Global instances
detector = AnomalyDetector()
digital_twin = DigitalTwinModel()
injector = FaultInjector()

# ─────────────────────────────────────────────
# Data Generation
# ─────────────────────────────────────────────

def get_base_readings(is_safe_mode: bool):
    if is_safe_mode:
        # AI Mitigation: Forces motor to low-power, safe state
        rpm = random.uniform(900, 1000)
        temp = random.uniform(45.0, 55.0)
        vib = random.uniform(0.5, 1.2)
        curr = random.uniform(5.0, 7.0)
    else:
        rpm = random.uniform(*NORMAL_RANGES["rpm"])
        temp = random.uniform(*NORMAL_RANGES["temperature"])
        vib = random.uniform(*NORMAL_RANGES["vibration"])
        curr = random.uniform(*NORMAL_RANGES["current"])
    return rpm, temp, vib, curr

def generate_reading() -> dict:
    injector.tick()
    
    # Get physical baseline (which is modified if AI stepped in)
    rpm, temp, vib, curr = get_base_readings(detector.in_safe_mode)
    
    # Inject persistent physical fault
    rpm, temp, vib, curr, fault_severity = injector.apply_fault(rpm, temp, vib, curr, detector.in_safe_mode)

    # Analyze through our modular systems
    analysis = detector.analyze(rpm, temp, vib, curr)
    twin_data = digital_twin.compare(rpm, temp, vib, curr)

    return {
        "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rpm":            round(rpm, 2),
        "temperature":    round(temp, 2),
        "vibration":      round(vib, 3),
        "current":        round(curr, 2),
        "health_score":   analysis["health_score"],
        "status":         analysis["status"],
        "anomaly_reason": analysis["anomaly_reason"],
        "recommendation": analysis["recommendation"],
        "ai_action":      analysis["ai_action"],
        "fault_type":     injector.active_fault,
        "fault_severity": fault_severity,
        "expected_rpm":   twin_data["expected_rpm"],
        "expected_temperature": twin_data["expected_temperature"],
        "expected_vibration": twin_data["expected_vibration"],
        "expected_current": twin_data["expected_current"],
        "deviation_score": twin_data["deviation_score"],
        "twin_status":    twin_data["twin_status"]
    }

# ─────────────────────────────────────────────
# CSV I/O
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
    # Write to temp file first, then atomically rename to prevent partial reads
    tmp_path = CSV_PATH + ".tmp"
    df.to_csv(tmp_path, index=False)
    
    # Retry loop to handle Windows file locks when Streamlit dashboard reads concurrently
    for i in range(10):
        try:
            os.replace(tmp_path, CSV_PATH)
            break
        except (PermissionError, OSError):
            if i == 9:
                raise
            time.sleep(0.05)

def append_reading(new_row: dict) -> pd.DataFrame:
    df = load_existing_data()
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    save_data(df)
    return df

# ─────────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────────
def run_generator() -> None:
    print("=" * 100)
    print("  Electric Motor Digital Triplet – Telemetry Generator")
    print(f"  Output : {CSV_PATH}")
    print("=" * 100)

    try:
        while True:
            row = generate_reading()
            df = append_reading(row)
            tag = f"[{row['status'].upper()}]".ljust(10)
            print(
                f"[{row['timestamp']}] {tag} | "
                f"Fault={row['fault_type']} ({row['fault_severity']}) | "
                f"AI_Safe={detector.in_safe_mode} | "
                f"Dev={row['deviation_score']}%"
            )
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n\nGenerator stopped.")

if __name__ == "__main__":
    run_generator()
