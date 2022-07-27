from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime

cl = Client()
cl.request_timeout = 5 # seconds
s = open('session.json')
session = json.load(s)
c = open("config.json")
config = json.load(c)
x = datetime.datetime.now()
today = datetime.datetime.now()

print("Datos de la sesión guardados en session.json")
print("Session ID: ", session['authorization_data']['sessionid'])
cl.login_by_sessionid(session['authorization_data']['sessionid'])
print(cl.user_id_from_username("rrrmn2"))
#print(cl.user_followers_gql_chunk(cl.user_id_from_username("rrrmn2"), 5, 6))
#print(cl.user_followers_gql_chunk(cl.user_id_from_username("rrrmn2"), 5, 6))
#user_followers_v1_chunk(user_id: int, max_amount: int = 0, max_id: str = "")
print(cl.user_followers_v1_chunk(cl.user_id_from_username("rrrmn2"), 1, 200))
print(cl.user_followers_v1_chunk(cl.user_id_from_username("rrrmn2"), 1, 200)[1])