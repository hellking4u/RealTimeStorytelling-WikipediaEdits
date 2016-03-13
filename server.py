#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Sets up the Main server along with the basic analytics dashboard.

"""
from flask import Flask
from flask import render_template
import json
import redis as rLib
import config
from scipy.stats import entropy
import operator
import json

application = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

redis = rLib.Redis(db=3) # distribution testing

@application.route("/")
def main():
    """
    The basic endpoint returns the main page with the Map and the markes of wikipedia edits.
    """
    return render_template('index.html')

@application.route("/analytics")
def hello():
    """
    Generates the analytics dashboard. This is made as generic as possible (within a couple of hours).
    It assumes the set of keys in the redis database to be from a categorical database.
    It iterates through the keys to generate a histogram, a listed percentage of categorical values,
    finds the entropy, and finds the probability of the next message (assuming categorical prior and no other 
        features.)


    The Entropy calculated is the Shannon Entropy.
    
    It also uses a generic structure of "listed_data", which can be used to put arbitrary data on the dashboard.

    example :

    listed_data['Calculated Entropy'] = round(calculated_entropy,2)

    this rounds the entropy and stores it with the key 'Calculated Entropy'. The key is used to display the value in the dashboard.
    """
    #generate data
    dataset = []
    total = 0

    listed_data = {} # Use this to add any arbitrary key-value data to be shown on the dashboard.

    datapoint_values = []

    for key in redis.keys('*'):
        value = redis.get(key)
        datapoint = {'x': key, 'y':float(value)}
        dataset.append(datapoint)
        datapoint_values.append(int(value))
        total += int(redis.get(key))

    # Calculate the Entropy using the scipy.stats.entropy function.
    calculated_entropy = entropy(datapoint_values)

    listed_data['Calculated Entropy'] = round(calculated_entropy,2)


    #get the next message prediction :

    # this set of lines is just to calculate the message with the highest number seen (thereby the highest probability)

    maximum = ["", 0]
    for elem in dataset:
        if elem['y'] > maximum[1]:
            maximum[0] = elem['x']
            maximum[1] = elem['y']


    # round off the probability to the 2nd place and send it.
    probability = round(float(maximum[1])/total,2)

    # The listed data uses a tiny technique to help format it more asthetically. It closes the previous span, writes down the text, and then repoens the
    # span. For further details, have a look at analytics.htm. (It's written in Jinja)
    listed_data['Next Predicted Message'] = "{0}</span> with probability <span class='emphasis'>{1}".format(maximum[0], probability)

    return render_template('analytics.htm', data = dataset, total = total, bullet_data=listed_data)

@application.route("/json")
def apiFunc():
    """
    API Endpoint to get the JSON values of the data shown on the dashboard. For further details,
    have a look at the hello() function.
    """
    #generate data
    dataset = []
    total = 0

    listed_data = {}

    datapoint_values = []
    for key in redis.keys('*'):
        value = redis.get(key)
        datapoint = {'x': key, 'y':float(value)}
        dataset.append(datapoint)
        datapoint_values.append(int(value))
        total += int(redis.get(key))


    # Calculate the Entropy using the scipy.stats.entropy function.
    calculated_entropy = entropy(datapoint_values)

    listed_data['entropy'] = round(calculated_entropy,2)

    maximum = ["", 0]
    for elem in dataset:
        if elem['y'] > maximum[1]:
            maximum[0] = elem['x']
            maximum[1] = elem['y']

    probability = round(float(maximum[1])/total,2)
    listed_data['next_message'] = [maximum[0], probability]

    return_value = dict()
    return_value['data'] = dataset
    return_value['total'] = total
    return_value['extra'] = listed_data
    return json.dumps(return_value)

if __name__ == "__main__":
    # the flask application is set to run in the production setting (port 80)

    # this is a *serious* security hazard in production systems, otherwise, it's fine.
    application.run(host='0.0.0.0', port=80, debug=True)
