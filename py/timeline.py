import time
import argparse
import mysql.connector
import ftplib
import json
from functions_minning import *

s = open("session.json")
session = json.load(s)

time = cl.get_timeline_feed()

print(time.keys())

for key, value in time.items():
    if key != 'feed_items':
        print(key, " -> ", value)
        print("[response] --------- ")
    elif key == 'feed_items':
        print("[feed] --------- ")
        for item_feed in time['feed_items']:
            for f_key, f_value in item_feed.items():
                if f_key == 'media_or_ad':
                    print("[media or ad] +++++")
                    #print(item_feed[f_key]['id'])
                    #print(item_feed[f_key]['pk'])
                    print(item_feed[f_key]['caption'])
                    #for media_item in item_feed[f_key].items():
                        #print(type(media_item))
                        #print(media_item)
                elif f_key == 'suggested_users':
                    print("[suggested users] +++++")
                    #print (len(item_feed[f_key]['suggestion_cards']))
                    #print(item_feed[f_key]['suggestion_cards'])
                    for user in item_feed[f_key]['suggestion_cards']:
                        for us_key, us_value in user.items():
                            if us_key == 'user_card':
                                print("[user card] +++++ ")
                                #print(us_key, " -> ", us_value)
                            if us_key == 'upsell_ci_card':
                                print("[upsell_ci_card] +++++ ")
                                print(us_key, " -> ", us_value)
