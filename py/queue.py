import mysql.connector
from functions_minning import *

c = open("config.json")
config = json.load(c)
x = datetime.datetime.now()
today = datetime.datetime.now()

def fetch(batch_size=2, sleep_time=5):
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
                       "WHERE 'waiting' in (status) "
                       "LIMIT 0, %s" % (batch_size))

        queue_batch = cursor.fetchall()

        for q in queue_batch:
            print(q)
            #cursor.execute("UPDATE queue SET status = 'working' WHERE id = %s" % (q[0]))
            idmb_userInfo(q[2], 4, 15, 0, 0)
            #cnx.commit()

        print("Pause of sleep_time: ", str(sleep_time))
        time.sleep(sleep_time)
        fetch(batch_size, sleep_time)


fetch(2, 1)