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
#print( cl.user_medias_paginated(cl.user_id_from_username(user_minning),20) )
print( cl.user_medias_paginated(cl.user_id_from_username(user_minning),2, "QVFES1NrU3EtcmdNekEzZXZuU0tJa1FLS2hsMUUtOGFsTm9HMXdrMXppVGQ4ZVpibHZCSE5tR1NSX1lqTm1JRWx1RWkwUFZKWHVFd0VXeWN2TWs2M1VvMA=="))
print( cl.user_medias_paginated(cl.user_id_from_username(user_minning),2, "QVFES1NrU3EtcmdNekEzZXZuU0tJa1FLS2hsMUUtOGFsTm9HMXdrMXppVGQ4ZVpibHZCSE5tR1NSX1lqTm1JRWx1RWkwUFZKWHVFd0VXeWN2TWs2M1VvMA==")[1] )

print("--- %s seconds ---" % (time.time() - start_time))