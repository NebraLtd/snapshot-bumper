# Program that stores blocks to database.

from time import sleep
# from tinydb import TinyDB, Query
import urllib.request
import json
from urllib.error import URLError, HTTPError
from pprint import pprint

import sqlite3
con = sqlite3.connect('block_cache.db')
cur = con.cursor()
# db = TinyDB('block_cache.json')

# Set last block variable as a starting point
lastBlock = 800641
blockchainHeight = 0

apiUrl = "https://api.helium.io/v1/blocks/"

# Get Blockchain Height

try:
    heightUrl = apiUrl +  "height"
    with urllib.request.urlopen(heightUrl) as response:
        heightJson = json.loads(response.read())
        blockchainHeight = (heightJson['data']['height'])
except HTTPError as e:
    #Most likely not generate yet. Sleep
    print("Waiting for request")

    sleep(2)

print(blockchainHeight)

# Getting latest entry

try:
    cur.execute('SELECT * FROM blocks ORDER BY height DESC')

    lastBlock = cur.fetchone()[4]
except TypeError as e:
    pass

print("Loading blocks into cache db")

while(lastBlock < blockchainHeight):
    blockUrl = apiUrl + str(lastBlock)
    try:
        with urllib.request.urlopen(blockUrl) as response:
            blockJson = json.loads(response.read())['data']
            #pprint(blockJson)
            cur.execute("insert into blocks values (?, ?, ?, ?, ?, ?)", (blockJson['transaction_count'], blockJson['time'], blockJson['snapshot_hash'], blockJson['prev_hash'], blockJson['height'], blockJson['hash']))
            con.commit()
    except HTTPError as e:
        #Most likely not generate yet. Sleep
        print("Waiting for request")
        sleep(2)
    except sqlite3.IntegrityError as e:
        print("Already in DB")
    print(lastBlock)
    lastBlock+=1
