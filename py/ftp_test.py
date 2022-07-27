import ftplib
import os
import json

f = open("config.json")
config = json.load(f)

ftp_server = ftplib.FTP(config["FTP"]["hostname"],config["FTP"]["username"],config["FTP"]["password"])

ftp_server.encoding = "utf-8"

filename = "config.json"

with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {filename}",file)

ftp_server.dir()

ftp_server.quit()