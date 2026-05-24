class AnomalyDetector:
    def __init__(self):
        self.degradation_penalty = 0
        self.anomaly_streak = 0
        self.in_safe_mode = False
        self.safe_mode_ticks = 0
        self.ai_action_taken = "None"

    def analyze(self, rpm: float, temp: float, vib: float, curr: float,
                pressure: float = 1013.25, color_cmd: str = "MONITORING") -> dict:
        """
        Analyzes telemetry values, computes a health score, and updates 
        predictive maintenance degradation state. Returns structured output.
        
        Supports additional parameters from MYOSA board:
        - pressure: atmospheric pressure in hPa from BMP180
        - color_cmd: maintenance command from APDS9960 color sensor
        """
        reason = "None"
        recommendation = "None"
        is_anomaly = False

        # ── MYOSA Color Command Override ──
        # RED_STOP is an authoritative emergency signal from the physical sensor
        if color_cmd == "RED_STOP":
            is_anomaly = True
            reason = "EMERGENCY STOP triggered via MYOSA color sensor"
            recommendation = "Immediate shutdown required. Inspect motor before restarting."
            self.ai_action_taken = "RED_STOP override active — motor flagged for emergency halt."

            # Force critical immediately
            final_health = max(0.0, 100.0 - 60 - self.degradation_penalty)
            return {
                "health_score": round(final_health, 1),
                "status": "critical",
                "anomaly_reason": reason,
                "recommendation": recommendation,
                "ai_action": self.ai_action_taken,
                "trigger_safe_mode": True
            }

        if color_cmd == "BLUE_MAINT":
            reason = "MAINTENANCE MODE triggered via MYOSA color sensor"
            recommendation = "System in maintenance mode. Reduced monitoring active."

        # ── Standard Threshold-Based Anomaly Detection ──
        if vib > 4.0:
            is_anomaly = True
            reason = "High vibration detected"
            recommendation = "Inspect bearing alignment and rotor balance"
        elif temp > 85.0:
            is_anomaly = True
            reason = "High temperature detected"
            recommendation = "Reduce thermal load, check cooling system"
        elif curr > 15.0:
            is_anomaly = True
            reason = "Current spike detected"
            recommendation = "Check motor load conditions and electrical supply"
        elif rpm < 1200 and not self.in_safe_mode:
            is_anomaly = True
            reason = "RPM drop detected"
            recommendation = "Inspect rotor performance and mechanical drag"

        # ── Pressure Anomaly Detection (MYOSA BMP180) ──
        if pressure < 950.0:
            is_anomaly = True
            reason = "Low atmospheric pressure detected"
            recommendation = "Check environmental sensor or altitude change"
        elif pressure > 1060.0:
            is_anomaly = True
            reason = "High atmospheric pressure detected"
            recommendation = "Verify BMP180 sensor calibration"

        # Raw base health computation
        rpm_penalty = min(abs(rpm - 1500) / 200 * 25, 25)
        temp_penalty = min(abs(temp - 65) / 30 * 25, 25)
        vib_penalty = min(abs(vib - 1.5) / 6 * 25, 25)
        curr_penalty = min(abs(curr - 10) / 12 * 25, 25)
        
        raw_health = 100 - (rpm_penalty + temp_penalty + vib_penalty + curr_penalty)

        # Predictive maintenance logic
        if is_anomaly:
            self.anomaly_streak += 1
            if self.anomaly_streak % 2 == 0:  # Penalty every 2 ticks of anomaly
                self.degradation_penalty += 1
                
            # Allow the fault to persist visually for a few seconds before AI steps in
            if self.anomaly_streak >= 5 and not self.in_safe_mode:
                self.in_safe_mode = True
                self.safe_mode_ticks = 15  # AI takes over for 15 seconds
                self.ai_action_taken = f"Autonomous mitigation active for {reason}. Motor parameters clamped to prevent critical failure."
        else:
            if not self.in_safe_mode:
                self.anomaly_streak = 0

        # Safe mode mitigates damage but flags a constant warning
        if self.in_safe_mode:
            status = "warning"
            reason = "Operating in AI Safe Mode (Mitigating Damage)"
            recommendation = "System autonomously stabilized. Maintenance required."
            
            self.safe_mode_ticks -= 1
            if self.safe_mode_ticks <= 0:
                self.in_safe_mode = False
                self.anomaly_streak = 0
                self.ai_action_taken = "None"
        else:
            if color_cmd != "BLUE_MAINT":
                self.ai_action_taken = "None"
            if is_anomaly:
                status = "critical"
            else:
                if raw_health - self.degradation_penalty < 80:
                    status = "warning"
                    if reason == "None":
                        reason = "System degradation accumulating"
                        recommendation = "Schedule routine inspection soon"
                else:
                    status = "normal"

        # BLUE_MAINT forces warning status even if readings are normal
        if color_cmd == "BLUE_MAINT" and status == "normal":
            status = "warning"

        final_health = max(0.0, min(100.0, raw_health - self.degradation_penalty))

        return {
            "health_score": round(final_health, 1),
            "status": status,
            "anomaly_reason": reason,
            "recommendation": recommendation,
            "ai_action": self.ai_action_taken,
            "trigger_safe_mode": self.in_safe_mode
        }
