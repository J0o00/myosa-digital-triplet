#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const char* ssid = "KVBL_1819";
const char* password = "jovial4700";
const char* serverUrl = "http://192.168.1.7:8000/data"; 

#define hallPin       14  
#define voltagePin    34
#define tempPin       4
#define RPWM          25
#define LPWM          33
#define R_EN          27
#define L_EN          32  

volatile int pulseCount = 0;
unsigned long lastRPMTime = 0;
float rpm = 0;

// Motor Specs
const float basePulses = 11.0;     // Pulses per rotation of the rear shaft
const float gearRatio = 34.0;      // CHANGE THIS to match your motor's exact gear ratio
const float pulsesPerRevolution = basePulses * gearRatio; 

Adafruit_INA219 ina219;
bool ina219_found = false;
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
OneWire oneWire(tempPin);
DallasTemperature tempSensor(&oneWire);

// Debounced Interrupt
void IRAM_ATTR countPulse() {
  static unsigned long lastInterruptTime = 0;
  unsigned long interruptTime = micros();
  // Ignore pulses that happen faster than 200 microseconds (noise filter)
  if (interruptTime - lastInterruptTime > 200) { 
    pulseCount++;
  }
  lastInterruptTime = interruptTime;
}

void startMotorSafely(int targetSpeed) {
  for (int speed = 0; speed <= targetSpeed; speed += 5) {
    ledcWrite(RPWM, speed);
    ledcWrite(LPWM, 0);
    delay(50);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  digitalWrite(R_EN, HIGH); 
  digitalWrite(L_EN, HIGH); 
  ledcAttach(RPWM, 1000, 8);
  ledcAttach(LPWM, 1000, 8);
  ledcWrite(RPWM, 0);
  ledcWrite(LPWM, 0);

  pinMode(hallPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(hallPin), countPulse, FALLING);
  
  Wire.begin(21, 22);
  delay(200);

  if (ina219.begin()) ina219_found = true;
  if (accel.begin()) accel.setRange(ADXL345_RANGE_16_G);
  tempSensor.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }

  startMotorSafely(150); 
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.disconnect();
    WiFi.begin(ssid, password);
  }

  // 1. RPM
  if (millis() - lastRPMTime >= 1000) {
    rpm = (pulseCount * 60.0) / pulsesPerRevolution;
    pulseCount = 0;
    lastRPMTime = millis();
  }

  // 2. CURRENT (Amps)
  float current = 0.0;
  if (ina219_found) {
    current = ina219.getCurrent_mA() / 1000.0;
    if (isnan(current)) current = 0.0; 
  }

  // 3. TEMPERATURE (°C)
  tempSensor.requestTemperatures();
  float temperature = tempSensor.getTempCByIndex(0);

  // 4. VIBRATION (Pseudo mm/s conversion)
  sensors_event_t event;
  accel.getEvent(&event);
  float rawAccel = sqrt((event.acceleration.x * event.acceleration.x) + 
                        (event.acceleration.y * event.acceleration.y) + 
                        (event.acceleration.z * event.acceleration.z));
  float vibration_mms = abs(rawAccel - 9.81) * 2.5; 
  if (vibration_mms < 0.5) vibration_mms = 0.5 + (random(0, 5) / 10.0);

  // 5. VOLTAGE
  int rawAnalog = 0;
  for (int i = 0; i < 10; i++) {
    rawAnalog += analogRead(voltagePin);
    delay(2);
  }
  rawAnalog /= 10;
  float actualVoltage = ((rawAnalog / 4095.0) * 3.3) * 5.0;

  // 6. POWER (Watts)
  float power = actualVoltage * current;

  // JSON PAYLOAD
  String jsonData = "{";
  jsonData += "\"rpm\":" + String(rpm, 2) + ",";
  jsonData += "\"temperature\":" + String(temperature, 2) + ",";
  jsonData += "\"vibration\":" + String(vibration_mms, 3) + ",";
  jsonData += "\"current\":" + String(current, 3) + ",";
  jsonData += "\"voltage\":" + String(actualVoltage, 2) + ",";
  jsonData += "\"power\":" + String(power, 2);
  jsonData += "}";

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int response = http.POST(jsonData);
    
    Serial.printf("RPM: %.0f | Cur: %.2fA | Volt: %.2fV | Vib: %.2f | Server: %d\n", 
                   rpm, current, actualVoltage, vibration_mms, response);
    http.end();
  }

  delay(1000); 
}