from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import time
import math
import os
import glob

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

def idmb_userInfo(username, request_timeout=2, media_pagination=30, media_minning=0, story_minning=0, sql=0, cnx=None, MUID=None, ftp=None):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    print("Username info for: ", username)
    info = cl.user_info_by_username(username)
    print(info)
    if media_minning == 1:
        print("Media minning active")
        print(media_pagination)
        print(info.media_count)
        idmb_userMedias(info.pk,media_pagination,info.media_count, cnx=cnx, ftp=ftp)
    else:
        print("Media minning not active")
    if story_minning == 1:
        print("Story minning active")
        idmb_userStories(info.pk)
    else:
        print("Story minning not active")
    if sql == 1:
        inner_cursor = cnx.cursor()
        following = json.dumps(idmb_userFollowing(username, 2))
        print(following)
        print("SQL insert active")
        #sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
        sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" #16
        val = (MUID, info.pk, info.username, info.full_name, info.is_private, info.following_count, info.follower_count, info.biography, info.external_url, info.account_type, info.is_business, info.public_email, info.city_id, info.city_name, following, datetime.datetime.now())
        inner_cursor.execute(sql, val)
    else:
        print("SQL insert not active")
    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_userMedias(user_id, media_pagination, media_count, iteration_no=None, iteration_counter=1, end_cursor=None, ftp=None, cnx=None):
    print("User Medias")
    ftp.cwd('/media')
    if directory_exists(user_id, ftp) is False:  # (or negate, whatever you prefer for readability)
        ftp.mkd(user_id)
    ftp.cwd(user_id)
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
            print(cnx)
            print("Media SQL Insert")

            for i, item in enumerate(list, 1):
                cnx.reconnect()
                inner_cursor = cnx.cursor()
                print(item.pk)
                user_dir = "tmp/" + user_id
                user_dir_exist = os.path.exists(user_dir)
                if not user_dir_exist:
                    #os.mkdir(user_dir)
                    os.makedirs(user_dir, 0o777)
                    print("The new directory is created!")

                media_conc = item.user.username + '_' + item.pk
                sql = "INSERT INTO data_media (user_id, pk, m_id, taken_at, media_type, product_type, location, comment_count, like_count, caption_text, media)" \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  #10
                val = (str(user_id), str(item.pk), str(item.id), item.taken_at, item.media_type, item.product_type, item.location, item.comment_count, item.like_count, item.caption_text, media_conc)

                inner_cursor.execute(sql, val)
                cnx.commit()
#From - https://adw0rd.github.io/instagrapi/usage-guide/media.html
#Photo - When media_type=1
#Video - When media_type=2 and product_type=feed
#IGTV - When media_type=2 and product_type=igtv
#Reel - When media_type=2 and product_type=clips
#Album - When media_type=8
                if item.media_type == 1:
                    cl.photo_download(int(item.pk), user_dir)
                elif item.media_type == 2 and item.product_type == 'feed':
                    cl.video_download(int(item.pk), user_dir)
                elif item.media_type == 2 and item.product_type == 'igtv':
                    cl.igtv_download(int(item.pk), user_dir)
                elif item.media_type == 2 and item.product_type == 'reel':
                    cl.clip_download(int(item.pk), user_dir)
                elif item.media_type == 8:
                    cl.album_download(int(item.pk), user_dir)
                else:
                    print("Err: media_type not defined")

                print(item.media_type, end="\n")
                print(item.product_type, end="\n")
                print(item.caption_text, end="\n")
                print(i, end="\n")
                print("----------------------------", end="\n")
# https://stackoverflow.com/questions/67520579/uploading-a-files-in-a-folder-to-ftp-using-python-ftplib
            print("uploading medias batch")
            toFTP = os.listdir(user_dir)
            for filename in toFTP:
                with open(os.path.join(user_dir, filename), 'rb') as file:  # Here I open the file using it's  full path
                    ftp.storbinary(f'STOR {filename}',
                                   file)  # Here I store the file in the FTP using only it's name as I intended
            #ftp.quit()
            #print("Deleting temporal batch files")
            #files = glob.glob(user_dir)
            #for f in files:
            #    os.remove(f)

            idmb_userMedias(user_id, media_pagination, media_count, iteration_no, iteration_counter + 1, cursor, ftp, cnx)
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
    #print(user_data.following_count)

    list = cl.user_following_v1(cl.user_id_from_username(username), amount)
    following_array = []
    for i, item in enumerate(list, 1):
        #print(item.username, end="\n")
        #print(i, end="\n")
        #print("----------------------------", end="\n")
        following_array.append(item.username)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return following_array

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

# Check if directory exists (in current location) - https://newbedev.com/create-missing-directories-in-ftplib-storbinary
def directory_exists(dir,ftp):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False