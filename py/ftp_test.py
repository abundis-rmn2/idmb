import ftplib
import json

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