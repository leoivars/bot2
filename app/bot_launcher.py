# # -*- coding: UTF-8 -*-

import os
import time
import datetime
from functions.load_config import get_bot_is_working_from_config

initial_date_working = datetime.datetime.now()
relaunch_count=0
bot_is_working = get_bot_is_working_from_config()

while bot_is_working:
    print('Laucher: launching...')

    os.system(f'python3 bot_main.py {relaunch_count} "{initial_date_working}"') 

    print('Launcher: bot_main.py ends')

    bot_is_working = get_bot_is_working_from_config()
    if bot_is_working:
        print("Launcher: wainting 10 seconds and relaunch")
        time.sleep(10)
        relaunch_count += 1
    
print('Launcher ends. Good Afternoon, Good Evening and Good Night.')    

