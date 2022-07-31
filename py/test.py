from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import time
start_time = time.time()

cl = Client()
cl.request_timeout = 2 # seconds
s = open('session.json')
session = json.load(s)
c = open("config.json")
config = json.load(c)
x = datetime.datetime.now()
today = datetime.datetime.now()

print("Datos de la sesión guardados en session.json")
print("Session ID: ", session['authorization_data']['sessionid'])
cl.login_by_sessionid(session['authorization_data']['sessionid'])
user_minning = "miss_lizzy_dizzy"
user_data = cl.user_info(cl.user_id_from_username(user_minning))
print(user_data.following_count)

list_following=cl.user_following_v1(cl.user_id_from_username(user_minning))

for i, item in enumerate(list_following,1):
    print(item, end = "\n")
    print(i, end = "\n")
    print("----------------------------", end = "\n")

print("--- %s seconds ---" % (time.time() - start_time))