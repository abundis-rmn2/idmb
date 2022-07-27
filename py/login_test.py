import argparse
from instagrapi import Client

parser = argparse.ArgumentParser(description='Paso de parámetros')
#El parámetro 1 es obligatorio que sea un entero
parser.add_argument("-usr", dest="IG_username", help="Instagram User")
#No forzamos ningún tipo para el parámetro 2
parser.add_argument("-pass", dest="IG_password", help="Instagram Password")
params = parser.parse_args()
print(params.IG_username)
print(params.IG_password)

cl = Client()
cl.login(params.IG_username, params.IG_password)
cl.dump_settings('session.json')
print("Datos de la sesión guardados en session.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))

import ftplib
import json

c = open("config.json")
config = json.load(c)
s = open("session.json")
session = json.load(s)

ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
ftp_server.encoding = "utf-8"
ftp_server.cwd('session_log')

filename = "session.json"
with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {session['authorization_data']['sessionid']}.json",file)

ftp_server.dir()

ftp_server.quit()

from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime

cl = Client()
s = open('session.json')
session = json.load(s)
c = open("config.json")
config = json.load(c)
x = datetime.datetime.now()
today = datetime.datetime.now()

print("Datos de la sesión guardados en session.json")
print("Session ID: ", session['authorization_data']['sessionid'])
cl.login_by_sessionid(session['authorization_data']['sessionid'])
print("Datos del usuario que inició sesión")
print("PK: ", cl.user_info(cl.user_id).pk)
print("Username: ", cl.user_info(cl.user_id).username)
print(cl.get_settings()['authorization_data']['sessionid'])
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

s.close()
c.close()