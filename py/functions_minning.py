from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import time

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

def idmb_userInfo(username, request_timeout=2):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    #time.sleep(5)
    print("Username info for: ", username)
    print(cl.user_info_by_username( username ))
    print("--- %s seconds ---" % (time.time() - start_time))

#Por el momento limitado a 100, lo ideal es que quede en 0 para que descargue todos
def idmb_userFollowing(username, request_timeout=2, amount="100"):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    user_data = cl.user_info(cl.user_id_from_username(username))
    print(user_data.following_count)

    list_following = cl.user_following_v1(cl.user_id_from_username(username), amount)

    for i, item in enumerate(list_following, 1):
        print(item, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_hashtagMediasTop(hashtag, request_timeout=2, amount=9):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    list_media_top = cl.hashtag_medias_top(hashtag, amount)

    for i, item in enumerate(list_media_top, 1):
        print(item, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    print("--- %s seconds ---" % (time.time() - start_time))

def countdown(n, n2):
    start_time = time.time()
    if n < n2:
        print(n)
        print(n2)
        time.sleep(n + 1)
        print("--- %s seconds ---" % (time.time() - start_time))
        countdown(n + 1, n2)