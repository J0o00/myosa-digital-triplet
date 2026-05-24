# MYOSA Digital Triplet

> AI-integrated industrial motor monitoring ecosystem with digital twin synchronization and predictive maintenance intelligence.

AI-powered industrial motor monitoring and predictive maintenance ecosystem using embedded systems, AI diagnostics, digital twins, and intelligent telemetry analysis.

<p align="center">
<img src="images/dashboard.png" width="1000"><br/>
<i>MYOSA Digital Triplet Dashboard</i>
</p>

---

# Acknowledgements

We thank the MYOSA community and organizers for providing the MYOSA Kit platform that enabled the development of this intelligent industrial monitoring ecosystem.

---

# Overview

MYOSA Digital Triplet is an AI-powered industrial motor monitoring system designed to analyze motor health in real time using:

* IoT
* embedded systems
* AI diagnostics
* digital twin synchronization
* predictive maintenance analytics

The project combines:

* ESP32 motor telemetry
* MYOSA edge intelligence
* FastAPI backend processing
* AI anomaly detection
* digital twin synchronization
* and a futuristic industrial dashboard interface

## Key Objectives

* Real-time industrial motor monitoring
* AI-powered anomaly detection
* Predictive maintenance analytics
* Digital Twin synchronization
* Intelligent edge sensing using MYOSA Kit
* Autonomous protection and safety logic

---

# Demo / Examples

## Images

<p align="center">
<img src="images/dashboard.png" width="900"><br/>
<i>MYOSA Digital Triplet Dashboard</i>
</p>

<p align="center">
<img src="images/fullsystem.jpg" width="900"><br/>
<i>Complete MYOSA Digital Triplet System</i>
</p>

<p align="center">
<img src="images/hardware.jpeg" width="900"><br/>
<i>Hardware Architecture and Sensor Integration</i>
</p>

<p align="center">
<img src="images/myosakit.jpeg" width="900"><br/>
<i>MYOSA Kit Edge Intelligence Node</i>
</p>

<p align="center">
<img src="images/telemetry.png" width="900"><br/>
<i>Real-Time Telemetry Visualization</i>
</p>

## Videos

* Local Repository Demo: [Watch Demo](videos/demo.mp4)
* Backup Drive Link: [Google Drive Video](https://drive.google.com/file/d/1IK0GVrevZfL-2KjDTvdgtj44JFnJ52pk/view?usp=sharing)

---

# Features (Detailed)

## 1. MYOSA Edge Intelligence

The MYOSA Kit acts as the intelligent edge sensing node of the ecosystem.

Implemented Features:

* Motion sensing using MPU6050
* Environmental sensing
* Edge telemetry generation
* Intelligent color-based commands
* Maintenance state signaling
* Real-time sensor telemetry

---

## 2. Color-Based Maintenance System

The APDS9960 sensor enables intelligent color interaction.

Color Actions:

* GREEN → Normal operation
* RED → Emergency stop
* BLUE → Maintenance mode
* YELLOW → Warning or future fault indication

This allows non-technical users to interact with the system visually without requiring dashboard access.

---

## 3. ESP32 Motor Telemetry Node

The ESP32 continuously monitors:

* Temperature
* Voltage
* Current
* RPM
* Vibration

The telemetry is transmitted wirelessly to the backend server for AI analysis and digital twin synchronization.

---

## 4. Digital Twin Synchronization

The system compares:

* Actual motor telemetry
  with
* Expected digital twin behavior

to detect:

* deviations
* anomalies
* synchronization loss
* and abnormal motor behavior

---

## 5. TRINITY AI

TRINITY AI is the intelligent industrial assistant integrated into the dashboard.

Features:

* telemetry-aware diagnostics
* anomaly explanations
* health analysis
* real-time monitoring insights
* intelligent system summaries

---

## 6. Predictive Maintenance

The dashboard performs:

* health scoring
* anomaly analysis
* risk detection
* predictive maintenance diagnostics
* autonomous protection logic

---

# Usage Instructions

## Start Backend

```bash
python backend/server.py
```

## Start Dashboard

```bash
streamlit run frontend/dashboard.py
```

## Run Telemetry Generator (Optional)

```bash
python backend/telemetry_generator.py
```

---

# Tech Stack

## Hardware

* ESP32
* MYOSA Kit
* BTS7960 Motor Driver
* Relay Module
* Industrial DC Geared Motor
* MPU6050
* APDS9960
* INA219
* Voltage Monitoring Circuit

## Software

* Python
* FastAPI
* Streamlit
* Plotly
* Embedded C++
* AI Diagnostics Engine

---

# Requirements / Installation

Install Python dependencies:

```bash
pip install fastapi streamlit pandas plotly requests
```

Hardware Requirements:

* ESP32
* MYOSA Kit
* BTS7960 Motor Driver
* Relay Module
* Sensors
* Industrial DC Motor

---

# File Structure

```plaintext
myosa-digital-triplet/
│
├── backend/
├── frontend/
├── esp32/
├── myosa/
├── images/
├── videos/
└── models/
```

---

# Future Improvements

Planned future updates:

* Machine learning-based fault prediction
* Advanced predictive maintenance
* Cloud analytics
* Autonomous maintenance scheduling
* Advanced digital twin simulation
* Improved RPM analytics
* Full Trinity AI voice interaction
* Industrial-scale deployment support

---

# License

This project is intended for educational, research, and innovation purposes.

---

# Contribution Notes

This project demonstrates how the MYOSA Kit can be effectively used for intelligent industrial monitoring, AI diagnostics, digital twin synchronization, and predictive maintenance systems in future industrial environments.
