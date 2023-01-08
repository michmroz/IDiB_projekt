import json
import time
import numpy as np
import traceback
import logging
from config import *

ser = start_serial()
cnx = connect_mysql()
cursor = cnx.cursor()

epoch_time_start = int(time.time())

#some default values to insert into database in case of the embedded measurement system is not connected:
temperature = "20"
humidity = "20"
light = "20"

#some default valuest to insert into database in case of the openweather request fail
temperature_out = "0"
humidity_out = "40"
pressure_out = "1000"
weather_description = "unknown"

url = build_weather_api_url()
while True:
  epoch_time_now = int(time.time())
  if epoch_time_now-epoch_time_start >= how_often_measure:
    epoch_time_start = epoch_time_now
  else:
    continue

  response = get_http_response(url) 

  # checking the status code of the request
  if response.status_code == 200:
    data = response.json()
    main = data['main']
    temperature_out = main['temp']
    humidity_out = main['humidity']
    pressure_out = main['pressure']
    weather_description = data['weather']
    previous_data_used_api = 0
    print(f"Temperature: {temperature_out}")
    print(f"Humidity: {humidity_out}")
    print(f"Pressure: {pressure_out}")
    print(f"Weather Report: {weather_description[0]['description']}")
  else:
    print(f"Error: http response status code = {response.status_code}")
    previous_data_used_api = 1
    
  ser.write("data_req_all".encode())
  time.sleep(3)
  try:
    if ser.inWaiting():
    #   print("ser.inWaiting() returned:")
    #   print(ser.inWaiting())
      line = ser.readline()
      print(line)
      data_ser = json.loads(line)
      temperature = data_ser['temperature']
      light = data_ser['light']
      humidity = get_humidity(humidity_out)
      previous_data_used_ser = 0
    else:
      print("serial port didn't respond, using last achieved data") 
      previous_data_used_ser = 1
    
  except Exception as e:
    logging.error(traceback.format_exc())
    previous_data_used = 1 
    
    
  insert_measurements_stmt = "INSERT INTO measurements (date, temperature, humidity, light, previous_data_used_ser) VALUES (%s, %s, %s, %s, %s)"
  insert_weather_stmt = "INSERT INTO weather (date, temperature_out, humidity_out, pressure_out, weather_description, previous_data_used_api) VALUES (%s, %s, %s, %s, %s, %s)"
  cursor.execute(insert_measurements_stmt, (epoch_time_now, temperature, humidity, light, previous_data_used_ser))
  cursor.execute(insert_weather_stmt, (epoch_time_now, temperature_out, humidity_out, pressure_out, weather_description[0]['description'], previous_data_used_api))

  cnx.commit()
