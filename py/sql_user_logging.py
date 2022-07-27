from instagrapi import Client
import os
import mysql.connector
from mysql.connector import errorcode
import json
import base64
from time import sleep
from random import randint
import re
import requests
import ftplib
import time
import sys
import shutil
from datetime import date
import datetime

cl = Client()
f = open('sesion.json')
data = json.load(f)
g = open("config.json")
config = json.load(g)
x = datetime.datetime.now()
today = datetime.datetime.now()
cl.login_by_sessionid(data['authorization_data']['sessionid'])

print("Datos de la sesión guardados en sesion.json")
print(cl.get_settings()['authorization_data']['sessionid'])
print("Datos del usuario que inició sesión")
print("PK: ", cl.user_info(cl.user_id).pk)
print("Username: ", cl.user_info(cl.user_id).username)
print("Session ID: ", data['authorization_data']['sessionid'])
print("Date: ", today)

try:
    cnx = mysql.connector.connect(user=config["SQL"]["username"],
                                  password=config["SQL"]["password"],
                                  host=config["SQL"]["hostname"],
                                  database=config["SQL"]["database"],
                                  )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
    else:
                print(err)
else:
    # get cursor object
    cursor = cnx.cursor()

    sql = "INSERT INTO user_logs (id, user, session, date)" \
                  "VALUES (%s, %s, %s, %s)" #4 entradas
    val = ("prueba", cl.user_info(cl.user_id).pk, cl.get_settings()['authorization_data']['sessionid'], today)
    cursor.execute(sql, val)

    cnx.commit()
    print('BD funciona')

f.close()