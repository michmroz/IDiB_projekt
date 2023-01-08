import math
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import traceback
import logging
from config_10 import *

cnx = connect_mysql()
cursor = cnx.cursor(dictionary=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/data')
async def handle_get_req(dateFrom: int=0, dateTo: int=0):
    if dateFrom == 0:
        dateFrom = oldest_measurement_timestamp
    if dateTo == 0: 
        dateTo = int(time.time())
    select_stmt=build_select_stmt(dateFrom, dateTo)                
    print(f"SELECT STATEMENT: {select_stmt}")
    select_success = False
    while select_success == 0:
        try:
            cursor.execute(select_stmt)
            select_res = cursor.fetchall()
            cnx.commit()
            select_success = True
        except Exception as e:
            logging.error(traceback.format_exc())
            #reconnect to mysql server:
            cnx = connect_mysql()
            cursor = cnx.cursor(dictionary=True)
            select_success = False
    
    
    return JSONResponse(content=jsonable_encoder(select_res))


def build_select_stmt(date_from: int=oldest_measurement_timestamp, date_to: int=0):
    stmt = (f"SELECT measurements.id, measurements.date, temperature, humidity, light, previous_data_used_ser,\
                   temperature_out, humidity_out, pressure_out, \
                   weather_description, previous_data_used_api \
                   FROM measurements INNER JOIN weather on measurements.id = weather.id \
                   WHERE measurements.date BETWEEN {date_from} AND {date_to}")

    rows_in_selected_period = math.ceil((float(date_to)-float(date_from))/float(how_often_measure))
    if (rows_in_selected_period > max_rows_returned):
        id_incr_value = math.floor(float(rows_in_selected_period)/float(max_rows_returned))
        stmt += (f"\nAND MOD(measurements.id, {id_incr_value}) = 0")
             
    return stmt
    