"""
process.py is a python script to take in JSON data from standard input and put it into redis for analysis.

The script takes in JSON data, adds the 't' and 'delta' keys, and pushes the JSON data out on stdout.

It uses Redis to store the data in (expirable) keys. The expiration time is set in the config file.

To use this file, Redis should be set up accurately.

On Mac :

Install using 'brew install redis'
Run 'redis-server'
"""
import json
import sys
import time
import redis as rLib

import config

last = 0
redis = rLib.Redis(db=15)

# We run the loop continuously and keep piping JSON input to output, with the changes.
# Note the lack of a try-except block. It's a (strict) expectation that the standard input
# will only have valid JSON.
while True:
    # Read a single line from standard input and parse it as JSON.
    line = sys.stdin.readline()
    d = json.loads(line)


    # time.time() returns the current epoch time (time since Jan 01 1970 00:00:00) and stores it as the key 't'.
    d['t'] = time.time()

    # If 'last' holds it initial value, update 'last' to hold the first timestamp recieved, and rerun the loop. 
    if last == 0 :
        last = d["t"]
        continue

    # Calculate the difference between the last message and the current message, and add it to the key 'delta' in the JSON.
    delta = d["t"] - last
    d['delta'] = delta

    #Update the 'last' variable to the time of the current message.
    last = d["t"]

    # add the data to redis. The key is the epoch time, and the value is the JSON dump of the entire data.
    # The expiration time is defined by the config file.
    redis.setex(d['t'], json.dumps(d), config.ANALYZE_TIME)

    # print out the JSON onto the standard output.
    print json.dumps(d)