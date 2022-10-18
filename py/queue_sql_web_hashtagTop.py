import time
import argparse
import mysql.connector
import ftplib
import json
from functions_minning import *

parser = argparse.ArgumentParser(description='Paso de parámetros')
parser.add_argument("-batch_size", dest="batch_size", help="Fetch from SQL queue list")
parser.add_argument("-starting", dest="starting", help="Jump to list")
parser.add_argument("-sleep_time", dest="sleep_time", help="Sleep time between Instagram requests")
parser.add_argument("-big_sleep", dest="big_sleep", help="Sleep between SQL fetch")
parser.add_argument("-MUID", dest="p_MUID", help="MUID to fetch")
params = parser.parse_args()
print(params)


c = open("config.json")
config = json.load(c)
s = open("session.json")
session = json.load(s)

#if os.path.isfile("proxy.txt"):
#    proxy = open("proxy.txt", "r")
#    proxy_address = proxy.read()
#    print(proxy_address)
#    cl.set_proxy(proxy_address)


# FTP Servidor

#ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
#ftp_server.encoding = "utf-8"
x = datetime.datetime.now()
today = datetime.datetime.now()

iteration_limit=21

def fetch(batch_size=10, sleep_time=5, big_sleep=30, err_counter=0, starting=0, counter=0, p_MUID=None):
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
        counter += 1
        print("iteration number", counter)
        print("Running queue bot with")
        print("batch_size: ", str(batch_size))
        print("sleep_time: ", str(sleep_time))
        print("big_sleep: ", str(big_sleep))
        print("MUID: ", str(p_MUID))
        cursor = cnx.cursor()
        if p_MUID == 'None':
            cursor.execute("SELECT * FROM queue "
                           "WHERE status IN ('waiting', 'working') "
                           "AND mining_type = 'hashtagTop'"
                           "LIMIT 0, %s" % (batch_size))
        else:
            cursor.execute("SELECT * FROM queue "
                           "WHERE status IN ('waiting', 'working') "
                           "AND MUID = '%s'" 
                           "LIMIT 0, %s" % (p_MUID, batch_size))

        queue_batch = cursor.fetchall()
        print("BatchCompleto: ",len(queue_batch))
        sliced_queue = queue_batch[starting:batch_size-5]
        print("BatchRecortado: ",len(sliced_queue))

        for q in sliced_queue:
            print("Pause of sleep_time: ", str(sleep_time))
            time.sleep(sleep_time)
            if q[4] == "user":
                print("Hashtag Top mining")
                #action its working @ queue_sql_web.py
            elif q[4] == "hashtagRecent":
                print("Hashtag Recent mining")
                err_counter += 1
                print(err_counter)
                print(q[7])
                print(q[2])
                print(q)
                if q[7] =="" or q[7] == botUsername or err_counter == 3:
                    print("Hashtag Recent mining")
                    updateTaskStatus(cnx, q[0], 'working')
                    idmb_hashtagMediasRecent(hashtag=q[2], request_timeout=sleep_time,amount=q[5], cnx=cnx,MUID=q[1], iteration_meta=q[3], iteration_no=q[8], queue=q)
                    #idmb_userInfo(q, sleep_time, 30, 0, 0, 1, cnx)
                    updateTaskStatus(cnx, q[0], 'done')
                    #err_counter= 0
            elif q[4] == "hashtagTop":
                print("Hashtag Top mining")
                print("Hashtag Recent mining")
                err_counter += 1
                print(err_counter)
                print(q[7])
                print(q[2])
                print(q)
                if q[7] =="" or q[7] == botUsername or err_counter == 3:
                    print("Hashtag Recent mining")
                    updateTaskStatus(cnx, q[0], 'working')
                    idmb_hashtagMediasTop(hashtag=q[2], request_timeout=sleep_time,amount=q[5], cnx=cnx,MUID=q[1], iteration_meta=q[3], iteration_no=q[8], queue=q)
                    #idmb_userInfo(q, sleep_time, 30, 0, 0, 1, cnx)
                    updateTaskStatus(cnx, q[0], 'done')
                    #err_counter= 0
            else:
                return

        print("Big sleep between tasks: ", big_sleep)
        time.sleep(int(big_sleep))
        print("New fetch() but with multiplied sleep_time")
        if sleep_time < 0.5 or sleep_time > 60:
            sleep_time = int(params.sleep_time)
        if big_sleep < 30 or big_sleep > 600:
            big_sleep = int(params.big_sleep)

        #sleep_time = round(sleep_time)
        list1 = [0.1, 1, 2, 3.5]
        sleep_time = sleep_time * random.choice(list1)
        big_sleep = big_sleep * random.choice(list1)
        print("randomized sleep_time", sleep_time)
        print("randomized big_sleep", big_sleep)

        if counter < iteration_limit:
            fetch(batch_size, sleep_time, big_sleep, err_counter, starting, counter, p_MUID)
        else:
            print("stop at iteration: ", iteration_limit)
            return

err_counter = 0
fetch(int(params.batch_size), int(params.sleep_time), int(params.big_sleep), err_counter, int(params.starting),0 , str(params.p_MUID))