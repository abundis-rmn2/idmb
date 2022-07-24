import os
from instagrapi import Client

cl = Client()
cl.load_settings('dump.json')
#cl.login('betitoprendido1', 'Automatico1!#*')
#cl.relogin()
cl.login_by_sessionid("51424674496%3AftJ398oNsYi8pt%3A0%3AAYdPiRJUD6x6EuJq1OFro4rWIUpOnpV2EIjx4Jss2Q")
#cl.dump_settings('dump.json')

cl.get_timeline_feed()  # check session
print(cl.get_settings())
print(cl.user_info(cl.user_id))

#user_id_scrapp = '1724903928'
#print(f'información del id: {user_id_scrapp}')
#print(cl.user_info(user_id_scrapp))
