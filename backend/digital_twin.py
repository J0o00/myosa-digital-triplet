import random

class DigitalTwinModel:
    """
    Simulates the theoretical "perfect" physical state of the electric motor.
    Provides baselines with healthy noise and calculates deviation from actual telemetry.
    
    Extended to include voltage, power, and pressure baselines for 
    ESP32 + MYOSA hardware integration.
    """
    def __init__(self):
        pass

    def generate_expected(self) -> dict:
        """Generates expected baseline telemetry with realistic 'healthy' noise."""
        expected_voltage = round(random.uniform(11.5, 12.5), 2)
        expected_current = round(random.uniform(9.5, 10.5), 2)
        return {
            "expected_rpm": round(random.uniform(1480, 1520), 2),
            "expected_temperature": round(random.uniform(63.0, 67.0), 2),
            "expected_vibration": round(random.uniform(1.2, 1.8), 3),
            "expected_current": expected_current,
            "expected_voltage": expected_voltage,
            "expected_power": round(expected_voltage * expected_current, 2),
            "expected_pressure": round(random.uniform(1005.0, 1020.0), 2),
        }

    def compare(self, actual_rpm: float, actual_temp: float,
                actual_vib: float, actual_curr: float,
                actual_voltage: float = 12.0, actual_power: float = 120.0,
                actual_pressure: float = 1013.25) -> dict:
        """
        Compares physical telemetry against the digital twin expectations.
        Returns expected baseline values, an aggregate deviation score, and synchronization status.
        
        Now includes voltage, power, and pressure in the deviation calculation
        (6-parameter average instead of 4).
        """
        expected = self.generate_expected()
        
        # Calculate percentage deviations against the expected baseline
        dev_rpm = abs(actual_rpm - expected["expected_rpm"]) / expected["expected_rpm"] if expected["expected_rpm"] else 0
        dev_temp = abs(actual_temp - expected["expected_temperature"]) / expected["expected_temperature"] if expected["expected_temperature"] else 0
        dev_vib = abs(actual_vib - expected["expected_vibration"]) / expected["expected_vibration"] if expected["expected_vibration"] else 0
        dev_curr = abs(actual_curr - expected["expected_current"]) / expected["expected_current"] if expected["expected_current"] else 0
        dev_volt = abs(actual_voltage - expected["expected_voltage"]) / expected["expected_voltage"] if expected["expected_voltage"] else 0
        dev_power = abs(actual_power - expected["expected_power"]) / expected["expected_power"] if expected["expected_power"] else 0
        dev_pres = abs(actual_pressure - expected["expected_pressure"]) / expected["expected_pressure"] if expected["expected_pressure"] else 0
        
        # Aggregate deviation score (average of percentage deviations, scaled to 0-100+)
        # Core motor params weighted more heavily than environmental
        core_dev = (dev_rpm + dev_temp + dev_vib + dev_curr + dev_volt + dev_power) / 6
        env_dev = dev_pres
        deviation_score = (core_dev * 0.85 + env_dev * 0.15) * 100
        
        # Evaluate synchronization status
        if deviation_score <= 10.0:
            twin_status = "Aligned"
        elif deviation_score <= 25.0:
            twin_status = "Diverging"
        else:
            twin_status = "Desynced"
            
        return {
            "expected_rpm": expected["expected_rpm"],
            "expected_temperature": expected["expected_temperature"],
            "expected_vibration": expected["expected_vibration"],
            "expected_current": expected["expected_current"],
            "expected_voltage": expected["expected_voltage"],
            "expected_power": expected["expected_power"],
            "expected_pressure": expected["expected_pressure"],
            "deviation_score": round(deviation_score, 1),
            "twin_status": twin_status
        }
