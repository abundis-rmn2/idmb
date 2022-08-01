from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import time
import math

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

def idmb_userInfo(username, request_timeout=2, media_pagination=30, media_minning=0, story_minning=0):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    print("Username info for: ", username)
    info = cl.user_info_by_username(username)
    print(info.biography)
    if media_minning == 1:
        print("Media minning active")
        print(media_pagination)
        print(info.media_count)
        idmb_userMedias(info.pk,media_pagination,info.media_count)
    else:
        print("Media minning not active")
    if story_minning == 1:
        print("Story minning active")
        idmb_userStories(info.pk)
    else:
        print("Story minning not active")

    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_userMedias(user_id, media_pagination, media_count, iteration_no=None, iteration_counter=1, end_cursor=None):
    print("User Medias")
    time.sleep(9)
    if media_pagination < media_count:
        iteration_no = math.ceil(media_count / media_pagination)
        print("Iterations needed", iteration_no)
        if iteration_counter <= iteration_no:
            print("Iteration counter", iteration_counter)
            if end_cursor == None:
                medias = cl.user_medias_paginated(user_id, media_pagination)
            else:
                medias = cl.user_medias_paginated(user_id, media_pagination, end_cursor)

            cursor = medias[1]
            list = medias[0]

            print(cursor)

            for i, item in enumerate(list, 1):
                print(item.caption_text, end="\n")
                print(i, end="\n")
                print("----------------------------", end="\n")

            idmb_userMedias(user_id, media_pagination, media_count, iteration_no, iteration_counter + 1, cursor)
    else:
        print("Iterations needed: 1")
        medias = cl.user_medias_paginated(user_id)
        list = medias[0]

        for i, item in enumerate(list, 1):
            print(item, end="\n")
            print(i, end="\n")
            print("----------------------------", end="\n")

def idmb_userStories(user_id):
    #Live Stories
    print("User Stories")
    list = cl.user_stories(user_id)
    for i, item in enumerate(list, 1):
        print(item.pk, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")


#Por el momento limitado a 100, lo ideal es que quede en 0 para que descargue todos
def idmb_userFollowing(username, request_timeout=2, amount=0):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    user_data = cl.user_info(cl.user_id_from_username(username))
    print(user_data.following_count)

    list = cl.user_following_v1(cl.user_id_from_username(username), amount)

    for i, item in enumerate(list, 1):
        print(item.username, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_hashtagMediasTop(hashtag, request_timeout=2, amount=9):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds

    #print(cl.hashtag_info(hashtag))

    list = cl.hashtag_medias_top(hashtag, amount)

    for i, item in enumerate(list, 1):
        print(item.caption_text, end="\n")
        print(item.location, end="\n")
        print(item.thumbnail_url, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_hashtagMediasRecent(hashtag, request_timeout=2, amount=9):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    list = cl.hashtag_medias_recent(hashtag, amount)

    #print(cl.hashtag_info(hashtag))

    for i, item in enumerate(list, 1):
        print(item.caption_text, end="\n")
        print(item.location, end="\n")
        print(item.thumbnail_url, end="\n")
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