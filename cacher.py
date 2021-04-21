# Program that stores blocks to database.

from time import sleep
from tinydb import TinyDB, Query
import urllib.request
import json
from urllib.error import URLError, HTTPError


db = TinyDB('block_cache.json')

# Set last block variable as a starting point
lastBlock = 0
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
# print(db.all()[0])
latestBlock = sorted(db.all(), key=lambda k: k['height'])

lastBlock = (int(latestBlock[-1]['height'])+1)

print("Loading blocks into cache db")

while(lastBlock < blockchainHeight):
    blockUrl = apiUrl + str(lastBlock)
    try:
        with urllib.request.urlopen(blockUrl) as response:
            blockJson = json.loads(response.read())['data']
            print(blockJson)
            db.insert(blockJson)

    except HTTPError as e:
        #Most likely not generate yet. Sleep
        print("Waiting for request")
        sleep(2)
    print(lastBlock)
    lastBlock+=1
