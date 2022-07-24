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
from datetime import datetime
import sys
import shutil

try:
    cnx = mysql.connector.connect(user='abundisc_xamuri',
                                  password='%8T[-kWX,E}N',
                                  host='abundis.com.mx',
                                  database='abundisc_idmb_nvi',
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

    sql = "INSERT INTO test (id, user, session, date)" \
                  "VALUES (%s, %s, %s, %s)" #4 entradas
    val = ("prueba", "prueba", "prueba", "Prueba")
    cursor.execute(sql, val)

    cnx.commit()
    print('BD funciona')