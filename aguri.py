import time
import sys

import os
import datetime
import json
import requests
from optparse import OptionParser

#python3 aguri.py -y 2016 -c 2

TARGET_DIR = "./image"
if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)

parser = OptionParser()

parser.add_option(
    '-y', '--year',
    action = 'store',
    type = 'str',
    dest = 'year',
)

parser.add_option(
    '-c', '--cours',
    action = 'store',
    type = 'str',
    dest = 'cours',
)

parser.set_defaults(
    year = 2017,
    cours_id = 1,
    sleep_sec = 30
)

options, args = parser.parse_args()

year = options.year
cours = options.cours
sleep_sec = options.sleep_sec


url = 'http://api.moemoe.tokyo/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)

create_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

for master in master_list:

    title = master['title']

    url = master['public_url']

    filename = create_time + "_" + str(master['id']) + ".png"

    print(title + " " + url + " " + filename)
