import argparse
from instagrapi import Client
import ftplib
import json
import os.path
import time


parser = argparse.ArgumentParser(description='Paso de parámetros')
#El parámetro 1 es obligatorio que sea un entero
parser.add_argument("-usr", dest="IG_username", help="Instagram User")
#No forzamos ningún tipo para el parámetro 2
parser.add_argument("-pass", dest="IG_password", help="Instagram Password")
#No forzamos ningún tipo para el parámetro 2
parser.add_argument("-proxy", dest="IG_proxy", help="Instagram Proxy")
params = parser.parse_args()
print(params.IG_username)
print(params.IG_password)
print(params.IG_proxy)

#revisar si existe el archivo session.json
session = './session.json'
check_file = os.path.isfile(session)
print(check_file)
if check_file == True:
    print("session.json exists")
    import timeline
    print(params.IG_username, " if IG timeline its printed means the session is ok")
    exit()

c = open("config.json")
config = json.load(c)
ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
ftp_server.encoding = "utf-8"
ftp_server.cwd('session_log')
ftp_server.dir()
print (ftp_server.nlst())
if f"{params.IG_username}.json" in ftp_server.nlst():
    # use FTP's RETR command to download the file
    #f"STOR {params.IG_username}.json"
    print("User has session.json in FTP downloading")
    with open("session.json", 'wb') as f:
        ftp_server.retrbinary(f"RETR {params.IG_username}.json", f.write)
    print("wait until complete download 10sec")
    time.sleep(1)
    ftp_server.quit()
    # open and read the file after the overwriting:
    f = open("session.json", "r")
    print(f.read())
    import timeline
    print(params.IG_username, " if IG timeline its printed means the session is ok")
    exit()

print("There's not session file local or ftp")
print("Where are going to log in")
cl = Client()
cl.login(params.IG_username, params.IG_password)
cl.dump_settings('session.json')
print("Datos de la sesión guardados en session.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))


s = open("session.json")
session = json.load(s)


filename = "session.json"
with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {params.IG_username}.json",file)
    print("Uploading sesson file")
ftp_server.dir()
ftp_server.quit()

import timeline
print(params.IG_username, " if IG timeline its printed means the session is ok")
