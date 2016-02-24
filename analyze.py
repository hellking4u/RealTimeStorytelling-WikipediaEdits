import redis
import json
import time
import sys

import sns

conn = redis.Redis(db=15)


last_alert = 0

def analyze_average(rate_of_stream):
    global last_alert
    if rate_of_stream < 3 and last_alert != "low":
        last_alert = "low"
        sns.sendNotification(rate_of_stream)
    if rate_of_stream >= 5 and last_alert != "high":
        last_alert = "high"
        sns.sendNotification(rate_of_stream)
while 1:

    pipe = conn.pipeline()

    keys = conn.keys()

    if len(keys):
        keys.sort()
        delta = float(keys[-1]) - float(keys[0])
        avg_rate = delta/len(keys)
        print avg_rate

        analyze_average(avg_rate)
        time.sleep(1)

