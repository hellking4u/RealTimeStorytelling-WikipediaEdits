import json
import sys
import time
import redis as rLib

import config

last = 0
redis = rLib.Redis(db=15)
while 1:
    line = sys.stdin.readline()
    d = json.loads(line)
    d['t'] = time.time()
    if last == 0 :
        last = d["t"]
        continue
    delta = d["t"] - last
    d['delta'] = delta
    last = d["t"]
    redis.setex(d['t'], json.dumps(d), config.ANALYZE_TIME)
    print json.dumps(d)