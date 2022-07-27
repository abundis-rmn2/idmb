import ftplib
import os

# Datos FTP
ftp_servidor = 'abundis.com.mx'
ftp_usuario = 'data_python@abundis.com.mx'
ftp_clave = '0xQbrS1pxXdf'
ftp_raiz = '/home/abundisc/'  # donde queremos subir el fichero

ftp_server = ftplib.FTP(ftp_servidor,ftp_usuario,ftp_clave)

ftp_server.encoding = "utf-8"

filename = "sesion.json"

with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {filename}",file)

ftp_server.dir()

ftp_server.quit()