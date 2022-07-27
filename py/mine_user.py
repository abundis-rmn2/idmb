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
#print(cl.user_info_by_username("rrrmn2").username)
print(cl.user_info_by_username("rrrmn2"))