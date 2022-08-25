import time

import mysql.connector
import ftplib
import json
from functions_minning import *

c = open("config.json")
config = json.load(c)
s = open("session.json")
session = json.load(s)

#if os.path.isfile("proxy.txt"):
#    proxy = open("proxy.txt", "r")
#    proxy_address = proxy.read()
#    print(proxy_address)
#    cl.set_proxy(proxy_address)

#ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
#ftp_server.encoding = "utf-8"
x = datetime.datetime.now()
today = datetime.datetime.now()
def fetch(batch_size=2, sleep_time=5, big_sleep=30, err_counter=0):
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
        print("Running queue bot with")
        print("batch_size: ", str(batch_size))
        print("sleep_time: ", str(sleep_time))
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM queue "
                       "WHERE status IN ('waiting', 'working') " 
                       "LIMIT 0, %s" % (batch_size))

        queue_batch = cursor.fetchall()

        for q in queue_batch:
            print("Pause of sleep_time: ", str(sleep_time))
            time.sleep(sleep_time)
            if q[4] == "user":
                err_counter += 1
                print(err_counter)
                print(q[7])
                print(q[2])
                if q[7] =="" or q[7] == botUsername or err_counter == 3:
                    print("User mining")
                    updateTaskStatus(cnx, q[0], 'working')
                    idmb_userInfo(q, sleep_time, 30, 0, 0, 1, cnx)
                    updateTaskStatus(cnx, q[0], 'done')
                    err_counter= 0
            elif q[4] == "hashtagRecent":
                print("Hashtag Recent mining")
            elif q[4] == "hashtagTop":
                print("Hashtag Top mining")
            else:
                return

        print("Big sleep between tasks")
        time.sleep(big_sleep)
        fetch(batch_size, sleep_time, big_sleep, err_counter)

err_counter = 0
fetch(1, 5, 30, err_counter)