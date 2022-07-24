import os
import json
from instagrapi import Client

cl = Client()
cl.login('betitoprendido1', 'Automatico1!#*')
cl.dump_settings('sesion.json')
print("Datos de la sesión guardados en sesion.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))