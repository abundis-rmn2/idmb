from instagrapi import Client
import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import time
import math
import os
import glob
import random
import ftplib
import re

cl = Client()
s = open('session.json')
session = json.load(s)
c = open("config.json")
config = json.load(c)
x = datetime.datetime.now()
today = datetime.datetime.now()

#if os.path.isfile("proxy.txt"):
#    proxy = open("proxy.txt", "r")
#    proxy_address = proxy.read()
#    print(proxy_address)
#    cl.set_proxy(proxy_address)

print("Datos de la sesión guardados en session.json")
print("Session ID: ", session['authorization_data']['sessionid'])
cl.login_by_sessionid(session['authorization_data']['sessionid'])
print(cl.account_info().dict()["username"])
botUsername = cl.account_info().dict()["username"]

def idmb_userInfo(queue, request_timeout=2, media_pagination=30, media_minning=0, story_minning=0, sql=0, cnx=None, ftp=None):
    username = queue[2]
    MUID = queue[1]
    iteration_no = queue[8]
    iteration_meta = queue[3]
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    print("Username info for: ", username)
    info = cl.user_info_by_username(username)
    print(info)
    if sql == 1:
        cnx.reconnect()
        cursor = cnx.cursor()
        following_array = idmb_userFollowing(username, 2, 3000)
        if not len(following_array) <= 3000:
            print("Following sliced insert")
            print("Slice array to ")
            following_dump = str(json.dumps(following_array[:3000]))
            print(following_dump)
            cnx.reconnect()
            print("SQL insert active")
            # sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
            sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, media_count, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 16
            val = (
            MUID, info.pk, info.username, info.full_name, info.is_private, info.media_count, info.following_count,
            info.follower_count, info.biography, info.external_url, info.account_type, info.is_business,
            info.public_email, info.city_id, info.city_name, following_dump, datetime.datetime.now())
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
        else:
            print("Following full insert")
            print(len(following_array))
            following_dump = json.dumps(following_array)
            print(following_dump)
            print("SQL insert active")
            cnx.reconnect()
            #sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
            sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, media_count, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" #16
            val = (MUID, info.pk, info.username, info.full_name, info.is_private,info.media_count, info.following_count, info.follower_count, info.biography, info.external_url, info.account_type, info.is_business, info.public_email, info.city_id, info.city_name, following_dump, datetime.datetime.now())
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
        if not iteration_no >= iteration_meta:
            print("Adding queue batch for next iteration")
            for follow in following_array:
                print(follow)
                sql = "INSERT INTO queue (MUID, seed_node, mining_depth, mining_type, created_at, hashtag_media_amount, iteration_no, status)" \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  # 7
                val = (
                MUID, follow, queue[3], queue[4], queue[5], datetime.datetime.now(), 1, 'waiting' )
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
    else:
        print("SQL insert not active")
    if media_minning == 1:
        print("Media minning active")
        print(media_pagination)
        print(info.media_count)
        idmb_userMedias(info.pk,media_pagination,info.media_count, cnx=cnx,)
    else:
        print("Media minning not active")
    if story_minning == 1:
        print("Story minning active")
        idmb_userStories(info.pk)
    else:
        print("Story minning not active")
    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_userInfo_public(queue, request_timeout=2, media_pagination=30, media_minning=0, story_minning=0, sql=0, cnx=None, ftp=None, proxy=None):
    cl.set_proxy(proxy)
    username = queue[2]
    MUID = queue[1]
    iteration_no = queue[8]
    iteration_meta = queue[3]
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    print("Username info for: ", username)
    info = cl.user_info_by_username(username)
    print(info)
    if sql == 1:
        cnx.reconnect()
        cursor = cnx.cursor()
        following_array = idmb_userFollowing_public(username, 2)
        if not len(following_array) <= 3000:
            print("Following sliced insert")
            print("Slice array to ")
            following_dump = str(json.dumps(following_array[:3000]))
            print(following_dump)
            cnx.reconnect()
            print("SQL insert active")
            # sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
            sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, media_count, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 16
            val = (
            MUID, info.pk, info.username, info.full_name, info.is_private, info.media_count, info.following_count,
            info.follower_count, info.biography, info.external_url, info.account_type, info.is_business,
            info.public_email, info.city_id, info.city_name, following_dump, datetime.datetime.now())
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
        else:
            print("Following full insert")
            print(len(following_array))
            following_dump = json.dumps(following_array)
            print(following_dump)
            print("SQL insert active")
            cnx.reconnect()
            #sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
            sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, media_count, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" #16
            val = (MUID, info.pk, info.username, info.full_name, info.is_private,info.media_count, info.following_count, info.follower_count, info.biography, info.external_url, info.account_type, info.is_business, info.public_email, info.city_id, info.city_name, following_dump, datetime.datetime.now())
            cursor.execute(sql, val)
            cnx.commit()
            cnx.close()
        if not iteration_no >= iteration_meta:
            print("Adding queue batch for next iteration")
            for follow in following_array:
                print(follow)
                sql = "INSERT INTO queue (MUID, seed_node, mining_depth, mining_type, created_at, hashtag_media_amount, iteration_no, status)" \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  # 7
                val = (
                MUID, follow, queue[3], queue[4], queue[5], datetime.datetime.now(), 1, 'waiting' )
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()
    else:
        print("SQL insert not active")
    if media_minning == 1:
        print("Media minning active")
        print(media_pagination)
        print(info.media_count)
        idmb_userMedias(info.pk,media_pagination,info.media_count, cnx=cnx,)
    else:
        print("Media minning not active")
    if story_minning == 1:
        print("Story minning active")
        idmb_userStories(info.pk)
    else:
        print("Story minning not active")
    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_userMedias(user_id, media_pagination, media_count, iteration_no=None, iteration_counter=1, end_cursor=None, cnx=None):
    print("User Medias")
    time.sleep(2)
    if media_pagination < media_count:
        iteration_no = math.ceil(media_count / media_pagination)
        print("Iterations needed", iteration_no)
        if iteration_counter <= iteration_no:
            print("Iteration counter", iteration_counter)
            medias = cl.user_medias_paginated(user_id, media_pagination, end_cursor)

            cursor = medias[1]
            list_arr = medias[0]
            print(cursor)
            print(cnx)
            print("Media SQL Insert")

            idmb_userSaveDataSQL(list_arr,cnx,user_id)
            idmb_userMedias(user_id, media_pagination, media_count, iteration_no, iteration_counter + 1, cursor, cnx)
    else:
        print("Iterations needed: 1")
        medias = cl.user_medias_paginated(user_id)
        list_arr = medias[0]

        idmb_userSaveDataSQL(list_arr,cnx,user_id)

def idmb_userSaveDataSQL(list_arr, cnx, user_id):
    for i, item in enumerate(list_arr, 1):
        cnx.reconnect()
        inner_cursor = cnx.cursor()
        print(item.pk)

        media_conc = item.user.username + '_' + item.pk
        sql = "INSERT INTO data_media (user_id, pk, m_id, taken_at, media_type, product_type, location, comment_count, like_count, caption_text, media)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 10
        val = (
        str(user_id), str(item.pk), str(item.id), item.taken_at, item.media_type, item.product_type, item.location,
        item.comment_count, item.like_count, item.caption_text, media_conc)

        inner_cursor.execute(sql, val)
        cnx.commit()

        print(item.media_type, end="\n")
        print(item.product_type, end="\n")
        print(item.caption_text, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

def idmb_userSaveDataFTPSQL(list_arr, cnx, user_id):
    user_dir = "tmp/" + user_id
    user_dir_exist = os.path.exists(user_dir)
    if not user_dir_exist:
        # os.mkdir(user_dir)
        os.makedirs(user_dir, 0o777)
        print("The user_dir was created")
    batch_dir = str(random.getrandbits(18))
    print(batch_dir)
    os.makedirs(user_dir + "/" + batch_dir, 0o777)
    working_dir = user_dir + "/" + batch_dir

    for i, item in enumerate(list_arr, 1):
        cnx.reconnect()
        inner_cursor = cnx.cursor()
        print(item.pk)

        media_conc = item.user.username + '_' + item.pk
        sql = "INSERT INTO data_media (user_id, pk, m_id, taken_at, media_type, product_type, location, comment_count, like_count, caption_text, media)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 10
        val = (
        str(user_id), str(item.pk), str(item.id), item.taken_at, item.media_type, item.product_type, item.location,
        item.comment_count, item.like_count, item.caption_text, media_conc)

        inner_cursor.execute(sql, val)
        cnx.commit()
        # From - https://adw0rd.github.io/instagrapi/usage-guide/media.html
        # Photo - When media_type=1
        # Video - When media_type=2 and product_type=feed
        # IGTV - When media_type=2 and product_type=igtv
        # Reel - When media_type=2 and product_type=clips
        # Album - When media_type=8
        if item.media_type == 1:
            cl.photo_download(int(item.pk), working_dir)
        elif item.media_type == 2 and item.product_type == 'feed':
            cl.video_download(int(item.pk), working_dir)
        elif item.media_type == 2 and item.product_type == 'igtv':
            cl.igtv_download(int(item.pk), working_dir)
        elif item.media_type == 2 and item.product_type == 'reel':
            cl.clip_download(int(item.pk), working_dir)
        elif item.media_type == 8:
            cl.album_download(int(item.pk), working_dir)
        else:
            print("Err: media_type not defined")

        print(item.media_type, end="\n")
        print(item.product_type, end="\n")
        print(item.caption_text, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    userDataUpload(working_dir, user_id)

def idmb_hashtagSaveDataFTPSQL(list_arr, cnx, hashtag_id, info, MUID, iteration_meta=0, iteration_no=0, queue=""):
    print(MUID)
    print(info)

    idmb_hashtagInfoSaveDataSQL(MUID, info, cnx)

    #Create tmp dir
    hashtag = "tmp/" + hashtag_id
    user_dir_exist = os.path.exists(hashtag)
    if not user_dir_exist:
        # os.mkdir(user_dir)
        os.makedirs(hashtag, 0o777)
        print("The user_dir was created")
    batch_dir = str(random.getrandbits(18))
    print(batch_dir)
    os.makedirs(hashtag + "/" + batch_dir, 0o777)
    working_dir = hashtag + "/" + batch_dir

    #SQL publication record insert
    for i, item in enumerate(list_arr, 1):
        print(item)
        cnx.reconnect()
        print("Inserting SQL record")
        print(item.pk)
        print("MUID")
        print(MUID)

        media_conc = item.user.username + '_' + item.pk
        hashtags_used = extract_hash_tags(item.caption_text)
        hashtags_obj = list(hashtags_used)
        hashtags_used = json.dumps(list(hashtags_used))
        print("Hashtags used")
        print(hashtags_used)

        sql = "INSERT INTO data_media (user_id, MUID, pk, m_id, taken_at, media_type, product_type, location, comment_count, like_count, caption_text, media, hashtags_used, hashtag_origin)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 13
        val = (
        str(item.user.username), MUID , str(item.pk), str(item.id), item.taken_at, item.media_type, item.product_type, str(item.location),
        item.comment_count, item.like_count, item.caption_text, media_conc, str(hashtags_used), hashtag_id)
        cnx.reconnect()
        inner_cursor = cnx.cursor()
        inner_cursor.execute(sql, val)
        inner_cursor.close()
        cnx.commit()

        print("Adding User info")
        usr_Info = cl.user_info_by_username(str(item.user.username));
        # sql = "INSERT INTO data_users (pk, username, full_name, is_private, profile_pic_url, profile_pic_url_hd, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, mined_at)" \
        user_sql = "INSERT INTO data_users (MUID, pk, username, full_name, is_private, media_count, following_count, follower_count, biography, external_url, account_type, is_business, public_email, city_id, city_name, following, mined_at)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 16
        user_val = (
            MUID, usr_Info.pk, usr_Info.username, usr_Info.full_name, usr_Info.is_private, usr_Info.media_count, usr_Info.following_count,
            usr_Info.follower_count, usr_Info.biography, usr_Info.external_url, usr_Info.account_type, usr_Info.is_business,
            usr_Info.public_email, usr_Info.city_id, usr_Info.city_name, '-', datetime.datetime.now())
        cnx.reconnect()
        user_inner_cursor = cnx.cursor()
        user_inner_cursor.execute(user_sql, user_val)
        user_inner_cursor.close()

        cnx.commit()
        cnx.close()
        #Add new queue tasks
        iteratorHashtag(iteration_no,iteration_meta, cnx, MUID, hashtags_obj, queue)


        # From - https://adw0rd.github.io/instagrapi/usage-guide/media.html
        # Photo - When media_type=1
        # Video - When media_type=2 and product_type=feed
        # IGTV - When media_type=2 and product_type=igtv
        # Reel - When media_type=2 and product_type=clips
        # Album - When media_type=8
        if item.media_type == 1:
            cl.photo_download(int(item.pk), working_dir)
        elif item.media_type == 2 and item.product_type == 'feed':
            #cl.video_download(int(item.pk), working_dir)
            print("no compatible media")
        elif item.media_type == 2 and item.product_type == 'igtv':
            #cl.igtv_download(int(item.pk), working_dir)
            print("no compatible media")
        elif item.media_type == 2 and item.product_type == 'reel':
            #cl.clip_download(int(item.pk), working_dir)
            print("no compatible media")
        elif item.media_type == 8:
            #cl.album_download(int(item.pk), working_dir)
            print("no compatible media")
        else:
            print("Err: media_type not defined")

        print(item.media_type, end="\n")
        print(item.product_type, end="\n")
        print(item.caption_text, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

    #FTP upload
    userDataUpload(working_dir, hashtag_id)

def idmb_userStories(user_id):
    #Live Stories
    print("User Stories")
    list_arr = cl.user_stories(user_id)
    for i, item in enumerate(list_arr, 1):
        print(item.pk, end="\n")
        print(i, end="\n")
        print("----------------------------", end="\n")

#Por el momento limitado a 100, lo ideal es que quede en 0 para que descargue todos
def idmb_userFollowing(username, request_timeout=2, amount=0):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    user_data = cl.user_info(cl.user_id_from_username(username))
    #print(user_data.following_count)

    list_arr = cl.user_following_v1(cl.user_id_from_username(username), amount)
    following_array = []
    for i, item in enumerate(list_arr, 1):
        #print(item.username, end="\n")
        #print(i, end="\n")
        #print("----------------------------", end="\n")
        following_array.append(item.username)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return following_array

def idmb_userFollowing_public(username, request_timeout=2, amount=0):
    start_time = time.time()
    cl.request_timeout = request_timeout  # seconds
    user_data = cl.user_info(cl.user_id_from_username(username))
    #print(user_data.following_count)

    list_arr = cl.user_following_v1(cl.user_id_from_username(username), amount)
    following_array = []
    for i, item in enumerate(list_arr, 1):
        #print(item.username, end="\n")
        #print(i, end="\n")
        #print("----------------------------", end="\n")
        following_array.append(item.username)
    #print("--- %s seconds ---" % (time.time() - start_time))
    return following_array

def idmb_hashtagMediasTop(hashtag, request_timeout=2, amount=9, cnx=None, ftp=None, MUID=None, iteration_meta=0, iteration_no=0, queue=""):
    start_time = time.time()
    print("MUID:")
    print(MUID)
    cl.request_timeout = request_timeout  # seconds
    info=cl.hashtag_info_v1(hashtag)
    list_arr = cl.hashtag_medias_top_v1(str(hashtag), int(amount))

    idmb_hashtagSaveDataFTPSQL(list_arr, cnx, hashtag, info, MUID, iteration_meta, iteration_no, queue)

    print("--- %s seconds ---" % (time.time() - start_time))

    #print(cl.hashtag_info(hashtag))

def idmb_hashtagMediasRecent(hashtag, request_timeout=2, amount=9, cnx=None, ftp=None, MUID=None, iteration_meta=0, iteration_no=0, queue=""):
    start_time = time.time()
    print("MUID:")
    print(MUID)
    cl.request_timeout = request_timeout  # seconds
    info=cl.hashtag_info_v1(hashtag)
    list_arr = cl.hashtag_medias_recent_v1(str(hashtag), int(amount))

    idmb_hashtagSaveDataFTPSQL(list_arr, cnx, hashtag, info, MUID, iteration_meta, iteration_no, queue)

    print("--- %s seconds ---" % (time.time() - start_time))

def idmb_hashtagInfoSaveDataSQL(MUID, info, cnx):
    cnx.reconnect()
    hashtag_data_cursor = cnx.cursor()
    if info.media_count == None:
        info.media_count = 0
    sql = "INSERT INTO data_recent_hashtags (MUID, hashtag, no_publications, IG_related_hashtags, hashtags_founded, mined_at)" \
          "VALUES (%s, %s, %s, %s, %s, %s)"  # 6
    val = (str(MUID), str(info.name), int(info.media_count) , "-", '-', datetime.datetime.now())
    hashtag_data_cursor.execute(sql, val)
    cnx.commit()
    cnx.close()

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

def userDataUpload(user_dir, user_id):
    ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
    ftp_server.encoding = "utf-8"
    #ftp_server.login()
    ftp_server.cwd('/media')
    if directory_exists(user_id, ftp_server) is False:  # (or negate, whatever you prefer for readability)
        print(user_id)
        print(user_dir)
        ftp_server.mkd(user_id)
    ftp_server.cwd(user_id)
    # https://stackoverflow.com/questions/67520579/uploading-a-files-in-a-folder-to-ftp-using-python-ftplib
    print("Uploading medias batch")
    toFTP = os.listdir(user_dir)
    for filename in toFTP:
        if filename not in ftp_server.nlst():
            print("Uploading: ")
            with open(os.path.join(user_dir, filename), 'rb') as file:  # Here I open the file using it's  full path
                ftp_server.storbinary(f'STOR {filename}', file)  # Here I store the file in the FTP using only it's name as I intended
            print(filename)
        else:
            print("File already exist")
    ftp_server.quit()
    # print("Deleting temporal batch files")
    # files = glob.glob(user_dir)
    # for f in files:
    #    os.remove(f)

def updateTaskStatus(cnx, task_id, task_status):
    cnx.reconnect()
    cursor = cnx.cursor()
    cursor.execute("UPDATE queue SET status = '%s' WHERE id = %s" % (task_status, task_id))
    cursor.execute("UPDATE queue SET bot_username = '%s' WHERE id = %s" % (botUsername, task_id))
    cnx.commit()

#From https://stackoverflow.com/questions/2527892/parsing-a-tweet-to-extract-hashtags-into-an-array
def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u0400-\u04FF" # russian
        u"\u0600-\u06ff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u0100-\u017f" #polish
                      "]+", re.UNICODE)
    cleanString = bytes(re.sub(emoj, '', data), 'utf-8').decode('utf-8', 'ignore')
    return cleanString

def iteratorHashtag(iteration_no, iteration_meta, cnx, MUID, hashtags_used, queue):
    print("Hashtag Iterator started for:")
    print(queue)
    #print(iteration_no, iteration_meta, cnx, MUID, hashtags_used, queue)
    if not iteration_no >= iteration_meta:
        print("Adding queue batch for next iteration:")
        for hashtag in hashtags_used:
            print(hashtag)
            cnx.reconnect()
            if not checkrecordHashtag(MUID, hashtag, cnx):
                cursor = cnx.cursor()
                sql = "INSERT INTO queue (MUID, seed_node, mining_depth, mining_type, created_at, hashtag_media_amount, iteration_no, status)" \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  # 8
                val = (
                    MUID, str(remove_emojis(hashtag)), iteration_meta, queue[4], datetime.datetime.now(), queue[5], iteration_no + 1, 'waiting')
                cursor.execute(sql, val)
                cnx.commit()
                cnx.close()

def cleanrecordHashtag(MUID, hashtag, cnx):
    print("Check task duplicates")
    inner_cursor = cnx.cursor()
    #SELECT * FROM queue WHERE MUID IN ('fr8_1_hashtagRecent_6_a981b121') AND seed_node IN ('fr8')
    inner_cursor.execute("SELECT * FROM queue WHERE MUID IN ('%s') AND seed_node IN ('%s')" % (MUID, hashtag))
    hashtags_arr = inner_cursor.fetchall()
    if hashtags_arr:
        print("Task duplicates found for:")
        print(hashtag)
        inner_cursor.execute("DELETE FROM queue WHERE MUID IN ('%s') AND seed_node IN ('%s')" % (MUID, hashtag))

def checkrecordHashtag(MUID, hashtag, cnx):
    print("Check task duplicates")
    inner_cursor = cnx.cursor()
    #SELECT * FROM queue WHERE MUID IN ('fr8_1_hashtagRecent_6_a981b121') AND seed_node IN ('fr8')

    inner_cursor.execute("SELECT * FROM queue WHERE MUID IN ('%s') AND seed_node IN ('%s')" % (MUID, str(remove_emojis(hashtag))))
    hashtags_arr = inner_cursor.fetchall()
    if hashtags_arr:
        return True
