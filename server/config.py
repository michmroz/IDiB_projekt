import logging
import traceback

########################################
how_often_measure = int(60);#[s] 
max_rows_returned = int(100)
oldest_measurement_timestamp = int(1640991600)

########################################
origins = [
    "http://localhost:4200",
]
########################################
import serial
import subprocess
def start_serial():
    subprocess.run(['sudo', 'chmod', '777', '/dev/ttyUSB0'])
    return serial.Serial('/dev/ttyUSB0', 9600)

########################################
import mysql.connector
def connect_mysql():
     return mysql.connector.connect(user='root', password='StudentPiwo123!',
                                    host='localhost', database='server_db')

########################################
def build_weather_api_url(base_url: str="https://api.openweathermap.org/data/2.5/weather?",
                          city: str="Poznan", language: str="pl", units: str="metric"):
    # paste your own:
    api_key = "7166596ad30578e4fbd90dc47a7a71c9"
    url = base_url + "q=" + city + "&lang=" + language + "&units=" + units + "&appid=" + api_key
    print(f"The openweather URL:\n{url}")
    return url

########################################
import requests
def get_http_response(URL):
  http_success = False
  while (http_success == False):
    try:
      response = requests.get(URL)
      http_success = True
    except Exception as e:
      logging.error(traceback.format_exc())
      print(f"http request failed, retrying: \
            {URL}")
      http_success = False

    return response
    

########################################
from numpy.random import randint
def get_humidity(humidity_out):
    #humidity = data_ser['humidity']
    #we don't have a humiditiy sensor, so we are simulating values:
    humidity = humidity_out - (randint(10,25))
    if humidity < 20:
        humidity = 20

    return humidity 


##########################################################
def insert_example_data(cursor, cnx, date_from: int=oldest_measurement_timestamp, date_to: int=0):
    current_date = date_from
    while (current_date < date_to):
        insert_measurements_stmt = \
            (f"INSERT INTO measurements (date, temperature, humidity, light, previous_data_used_ser) \
            VALUES({current_date}, 20, 30, 50, TRUE)")
        insert_weather_stmt = \
            (f"INSERT INTO weather (date, temperature_out, humidity_out, pressure_out, weather_description, previous_data_used_api) \
            VALUES({current_date}, 5, 40, 1000, \"pada albo nie, nie wiem\", TRUE)")
        # print(f"INSERT1 = '{insert_measurements_stmt}'")
        # print(f"INSERT2 = '{insert_weather_stmt}'")
        current_date += how_often_measure
        cursor.execute(insert_measurements_stmt)
        cursor.execute(insert_weather_stmt)


    cnx.commit()
       


