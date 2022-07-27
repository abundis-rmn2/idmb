import argparse
from instagrapi import Client

parser = argparse.ArgumentParser(description='Paso de parámetros')
#El parámetro 1 es obligatorio que sea un entero
parser.add_argument("-usr", dest="IG_username", help="Instagram User")
#No forzamos ningún tipo para el parámetro 2
parser.add_argument("-pass", dest="IG_password", help="Instagram Password")
params = parser.parse_args()
print(params.IG_username)
print(params.IG_password)

cl = Client()
cl.login(params.IG_username, params.IG_password)
cl.dump_settings('sesion.json')
print("Datos de la sesión guardados en sesion.json")
print(cl.get_settings())
print("Datos del usuario que inició sesión")
print(cl.user_info(cl.user_id))