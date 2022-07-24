import os
from instagrapi import Client


cl = Client()
user_id_scrapp = '1724903928'

print(f'información del id: {user_id_scrapp}')
print(cl.user_info(user_id_scrapp))