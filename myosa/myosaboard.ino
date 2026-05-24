#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_APDS9960.h>
#include <Adafruit_BMP085.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* ssid = "KVBL_1819";
const char* password = "jovial4700";
const char* serverUrl = "http://192.168.1.7:8000/edge"; 

Adafruit_APDS9960 apds;
Adafruit_BMP085 bmp;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

String maintenanceCommand = "MONITORING";
int displayPage = 0; 

bool mpu_ok = false;
bool bmp_ok = false;
bool apds_ok = false;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  delay(1000); 

  Serial.println("\n--- MYOSA KIT INITIALIZATION ---");

  // 1. OLED Setup
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("❌ OLED: FAILED");
  } else {
    display.clearDisplay(); display.setTextSize(1); display.setTextColor(WHITE);
    display.setCursor(0, 10); display.println("MYOSA Booting..."); display.display();
  }

  // 2. MPU6050 Setup (DIRECT I2C BYPASS)
  Wire.beginTransmission(0x69);
  Wire.write(0x6B);  // Target the Power Management Register
  Wire.write(0);     // Write 0 to wake it up
  if (Wire.endTransmission() == 0) {
    Serial.println("✅ MPU6050 (0x69): READY (Direct Mode)");
    mpu_ok = true;
  } else {
    Serial.println("❌ MPU6050: FAILED");
  }

  // 3. APDS9960 Setup
  if(!apds.begin()){
    Serial.println("❌ APDS9960: FAILED");
  } else {
    Serial.println("✅ APDS9960: READY");
    apds.enableProximity(true);
    apds_ok = true;
  }

  // 4. BMP180 Setup
  if (!bmp.begin()) {
    Serial.println("❌ BMP180: FAILED");
  } else {
    Serial.println("✅ BMP180: READY");
    bmp_ok = true;
  }

  // 5. WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\n✅ WiFi Connected!");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.disconnect();
    WiFi.begin(ssid, password);
  }

  // --- 1. MPU6050 (DIRECT READ) & BMP180 ---
  float vX = 0, vY = 0, vZ = 0, edge_vib = 0;
  
  if (mpu_ok) {
    Wire.beginTransmission(0x69);
    Wire.write(0x3B); // Start reading at register 0x3B (Accel X)
    Wire.endTransmission(false);
    Wire.requestFrom((uint16_t)0x69, (uint8_t)6, (uint8_t)true); // Request 6 bytes

    if (Wire.available() == 6) {
      int16_t ax = (Wire.read() << 8 | Wire.read());
      int16_t ay = (Wire.read() << 8 | Wire.read());
      int16_t az = (Wire.read() << 8 | Wire.read());

      // Convert raw data to m/s^2
      vX = (ax / 16384.0) * 9.81;
      vY = (ay / 16384.0) * 9.81;
      vZ = (az / 16384.0) * 9.81;
      edge_vib = sqrt((vX * vX) + (vY * vY) + (vZ * vZ));
    }
  }

  float pressure = 0, env_temp = 0;
  if (bmp_ok) {
    pressure = bmp.readPressure() / 100.0; 
    env_temp = bmp.readTemperature();
  }

  // --- 2. APDS9960 SMART-SWITCHER ---
  uint16_t r = 0, gr = 0, b = 0, c = 0;
  if (apds_ok) {
    apds.enableGesture(false);
    apds.enableColor(true);
    delay(50); 
    
    if (apds.colorDataReady()) {
      apds.getColorData(&r, &gr, &b, &c);
      if (c > 30) { 
        if (gr > r && gr > b) maintenanceCommand = "GREEN_RUN";     
        else if (r > gr && r > b) maintenanceCommand = "RED_STOP";      
        else if (b > r && b > gr) maintenanceCommand = "BLUE_MAINT";    
      }
    }

    apds.enableColor(false);
    apds.enableGesture(true);
    uint8_t gesture = apds.readGesture();
    if (gesture == APDS9960_LEFT || gesture == APDS9960_DOWN) {
      displayPage--;
      if (displayPage < 0) displayPage = 2; 
    } 
    else if (gesture == APDS9960_RIGHT || gesture == APDS9960_UP) {
      displayPage++;
      if (displayPage > 2) displayPage = 0; 
    }
  }

  // --- 3. OLED DISPLAY ---
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  if (displayPage == 0) {
    display.println("MYOSA HUB: OVERVIEW");
    display.print("Cmd: "); display.println(maintenanceCommand);
    display.print("Pres:"); display.print(pressure); display.println(" hPa");
    display.print("Vib: "); display.println(edge_vib);
  } else if (displayPage == 1) {
    display.println("COMMAND STATUS:");
    display.setCursor(0, 25);
    display.setTextSize(2); 
    display.print(maintenanceCommand);
  } else if (displayPage == 2) {
    display.println("ENVIRONMENT:");
    display.setCursor(0, 25);
    display.setTextSize(2); 
    display.print(pressure, 1);
  }
  display.display();

  // --- 4. PRINT TO SERIAL MONITOR ---
  Serial.println("============= MYOSA LIVE DATA =============");
  Serial.printf("[BMP180]   Temp: %.2f *C  | Pressure: %.2f hPa\n", env_temp, pressure);
  Serial.printf("[MPU6050]  X: %.2f  Y: %.2f  Z: %.2f | Vib Mag: %.2f\n", vX, vY, vZ, edge_vib);
  Serial.printf("[APDS9960] R: %d  G: %d  B: %d  C: %d | Cmd: %s\n", r, gr, b, c, maintenanceCommand.c_str());
  
  // --- 5. SEND TO LAPTOP ---
  String jsonData = "{";
  jsonData += "\"device\":\"myosa_edge_node\",";
  jsonData += "\"pressure\":" + String(pressure, 2) + ",";
  jsonData += "\"edge_vibration\":" + String(edge_vib, 2) + ",";
  jsonData += "\"color_cmd\":\"" + maintenanceCommand + "\"";
  jsonData += "}";

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int response = http.POST(jsonData);
    Serial.printf("[NETWORK]  Page: %d | Server Code: %d\n", displayPage, response);
    http.end();
  }
  Serial.println("===========================================\n");

  delay(200); 
}