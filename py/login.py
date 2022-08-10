import argparse
from instagrapi import Client
import ftplib
import json

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

cl = Client()
cl.set_proxy("socks5://4g.hydraproxy.com:55374")
cl.login(params.IG_username, params.IG_password)
cl.dump_settings('session.json')
print("Datos de la sesión guardados en session.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))

c = open("config.json")
config = json.load(c)
s = open("session.json")
session = json.load(s)

ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])
ftp_server.encoding = "utf-8"
ftp_server.cwd('session_log')

filename = "session.json"
with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {session['authorization_data']['sessionid']}.json",file)

ftp_server.dir()

ftp_server.quit()
