"""
Module to analyze rate of stream on Redis and notify using SNS if the rate is above (or below) a certain threshhold.
"""
import redis
import json
import time
import sys

import sns
import config

conn = redis.Redis(db=15)


last_alert = 0

def analyze_average(rate_of_stream):
    global last_alert
    if rate_of_stream < config.LOW_RATE and last_alert != "low":
        last_alert = "low"
        sns.sendNotification(rate_of_stream)
    if rate_of_stream >= config.HIGH_RATE and last_alert != "high":
        last_alert = "high"
        sns.sendNotification(rate_of_stream)
while 1:

    pipe = conn.pipeline()

    keys = conn.keys()

    if len(keys):
        keys.sort()
        # Find the delta value between the last key (the one added most recently) and the 
        # first key (the oldest key). This would give us the entire time range between them
        delta = float(keys[-1]) - float(keys[0])

        # calculate the average rate of update by divinging the total time (delta) with the 
        # total number of keys we have
        avg_rate = delta/len(keys)
        print avg_rate

        analyze_average(avg_rate)
        time.sleep(1)

