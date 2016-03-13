"""
Module to analyze rate of stream on Redis and notify using SNS if the rate is above (or below) a certain threshhold.
"""
import redis
import json
import time
import sys
from scipy.stats import entropy

import sns
import config

conn = redis.Redis(db=15)


last_alert = 0

def analyze_average(rate_of_stream):
    """
    Function to analyze rate of stream on Redis and notify using SNS if the rate is above (or below) a certain threshhold.
    """
    global last_alert
    if rate_of_stream < config.LOW_RATE and last_alert != "low":
        last_alert = "low"
        sns.sendNotification(rate_of_stream)
    if rate_of_stream >= config.HIGH_RATE and last_alert != "high":
        last_alert = "high"
        sns.sendNotification(rate_of_stream)


last_entropy_alert = 0
def analyze_entropy(redis_db_id=3):
    """
    Function to analyze entropy of categorical distribution on Redis and notify using SNS 
    if the rate is above (or below) a certain threshhold.

    The Entropy calculated is the Shannon Entropy.

    The parameter redis_db_id is used to pick the Redis database which holds the categorical distribution.

    Since the entropy should remain fairly balanced, any variation in entropy between the values is worth noticing.

    Also, since there is also a decrement.py script that constantly decrements the redis database, the entropy of

    the data is not stationary (which it would have been if we kept adding tons of data without removing the old), 
    and hence any abnormal values of entropy are interesting things to note.
    
    """
    global last_entropy_alert
    message = "We noticed an unusual entropy rate of {0}. It should ideally be between {1} and {2}."
    distribution_db = redis.Redis(db=redis_db_id)


    # Get the data from Redis to calculate the entropy
    datapoint_values = []
    total = 0
    for key in distribution_db.keys('*'):
        value = distribution_db.get(key)
        datapoint_values.append(int(value))
        total += int(value)


    # Calculate the Entropy using the scipy.stats.entropy function.
    calculated_entropy = entropy(datapoint_values)

    #format the meassage
    message = message.format(calculated_entropy, config.ENTROPY_LOW, config.ENTROPY_HIGH)


    if calculated_entropy < config.ENTROPY_LOW and last_entropy_alert != "low":
        last_entropy_alert = "low"
        sns.sendNotification(message, subject='Unusually Low Entropy')
    if calculated_entropy >= config.ENTROPY_HIGH and last_entropy_alert != "high":
        last_entropy_alert = "high"
        sns.sendNotification(message, subject='Unusual High Entropy')




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

        # analyze_average(avg_rate)
    analyze_entropy()
    time.sleep(1)

