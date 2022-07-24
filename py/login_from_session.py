import os
import json
from instagrapi import Client

cl = Client()
f = open('sesion.json')
data = json.load(f)

print (data['authorization_data']['sessionid'])
cl.login_by_sessionid(data['authorization_data']['sessionid'])

print("Datos de la sesión guardados en sesion.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))

f.close()