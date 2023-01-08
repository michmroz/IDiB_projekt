#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_BMP280.h>

BH1750 lightMeter;
Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  lightMeter.begin();
  unsigned status = bmp.begin(0x76);
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(),16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }
}

void loop() {
    while(!Serial.available()) {}
    delay(5);
    String req = Serial.readString();
    req.trim();
    if(req == "data_req_all") {
      StaticJsonDocument<400> doc;
      doc["temperature"] = getTemperature();
      doc["humidity"] = getHumidity();  
      doc["light"] = getLight();
      serializeJson(doc, Serial);
      Serial.println();
    }
}

String getTemperature() {
  return String(bmp.readTemperature(), 2);
}

String getLight() {
  return String(lightMeter.readLightLevel(), 2);
}

String getHumidity() {
  //brak sprawnego czujnika
  return "40.0";
}

