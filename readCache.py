import sqlite3
import datetime
import urllib.request
import json
import base64
from urllib.error import URLError, HTTPError
con = sqlite3.connect('/opt/nebrascripts/snapshot-bumper/block_cache.db')
cur = con.cursor()

blockchainHeight = 0

apiUrl = "https://api.helium.io/v1/blocks/"

# Get Blockchain Height

try:
    heightUrl = apiUrl +  "height"
    with urllib.request.urlopen(heightUrl) as response:
        heightJson = json.loads(response.read())
        blockchainHeight = (heightJson['data']['height'])
except HTTPError as e:
    # Most likely not generate yet. Sleep
    print("Waiting for request")

    sleep(2)

try:
    cur.execute('SELECT * FROM blocks WHERE snapshot_hash IS NOT "" ORDER BY height DESC')

    lastBlessedBlock = cur.fetchone()
except TypeError as e:
    pass
    
try:
    cur.execute('SELECT * FROM blocks ORDER BY height DESC')

    lastBlock = cur.fetchone()
except TypeError as e:
    pass

# print(lastBlock)
date = datetime.datetime.fromtimestamp(lastBlessedBlock[1]).strftime("%m/%d/%Y, %H:%M:%S")
print("Last Blessed Block: " + str(lastBlessedBlock[4]))
print("Last Blessed Block Date: " + date)
print(str(blockchainHeight-lastBlock[4]) + " Blocks left to sync")
snapshot_hash = lastBlessedBlock[2]
snapshot_hash += "=" * ((3- len(snapshot_hash) % 3) % 3)
hashArray = list(base64.urlsafe_b64decode(snapshot_hash))
# print(hashArray)
hashString = ','.join(str(e) for e in hashArray)
#print(hashString)
with open('baseConfig.config', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('bsbheight', str(lastBlessedBlock[4]))
filedata = filedata.replace('bsbhash', str(hashString))

# Write the file out again
with open('docker.config', 'w') as file:
  file.write(filedata)
