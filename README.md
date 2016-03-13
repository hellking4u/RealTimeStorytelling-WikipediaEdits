# RealTimeStorytelling-WikipediaEdits
A map showing anonymous edits made to Wikipedia in real time.

EDIT : Now also includes an analytics dashboard.

### The Map
![alt tag](https://raw.githubusercontent.com/hellking4u/RealTimeStorytelling-WikipediaEdits/master/screen1.png)

### The Analytics Dashboard
![alt tag](https://raw.githubusercontent.com/hellking4u/RealTimeStorytelling-WikipediaEdits/master/screen2.png)
## Running the Code
#### Websocket Server
```
websocketd --port 5000 python -u ws.py
```
Note the ```-u``` after python. This forces python to work with unbuffered stdout, which is what we want when using it with websocketd.

#### Web Server
```
 python -m SimpleHTTPServer
```

Python 3 users on Windows should use the http.server module.

```
python -m http.server [<portNo>]
```

## Stream Description
The aim of the project was to try and map out geolocatable wikipedia edits in real time. Fortunately, *Wikipedia* publishes it's recent changes in an IRC feed (details of which can be found here : ```https://meta.wikimedia.org/wiki/IRC/Channels#Wikipedia```). This saves a tremendous amount of time as we need not poll the service. To make our lives easier still, a github user **hatnote** has create a repo to consume this IRC feed and create a public websocket URL to consume. The repo can be found here : ```https://github.com/hatnote/wikimon```.

The websocket stream has a JSON like description, with multiple required fields. [1]
```json
    {"is_minor": false,
     "page_title": "Template:Citation needed/testcases",
     "url": "http://en.wikipedia.org/w/index.php?diff=553804313&oldid=479472901",
     "is_unpatrolled": false,
     "is_bot": false,
     "is_new": false,
     "summary": null,
     "flags": null,
     "user": "98.172.160.184",
     "is_anon": true,
     "ns": "Template",
     "change_size": "+42"}
    
    {"is_minor": true,
     "page_title": "Generalized anxiety disorder",
     "url": "http://en.wikipedia.org/w/index.php?diff=553804315&oldid=553370901",
     "is_unpatrolled": false,
     "is_bot": false,
     "is_new": false,
     "summary": "minor editing in sentences.",
     "flags": "M",
     "user": "BriannaMaxim",
     "is_anon": false,
     "ns": "Main",
     "change_size": "+1"}
```
## Stream Processing
We use the *Wikimon* websocket connection to recieve real-time edits. We filter the data which is actually a 'Page' edit and not an edit on the 'Talk' page or 'Special' page. We consequently filter on anonymous edits as they contain the geolocation of the editor. While tracking registered edits might be feasible, it would entail significantly more probing. Limiting tracking to anonymous edits means we tap into approximately 15% of the total stream, but it also makes the stream a more manageable size, with about 1 edit per second.

The stream is handled using Python using the Autobahn (asyncio) library. The code to recieve messages on a websocket stream is partly taken from the Autobahn Example 'echo'. ```https://github.com/crossbario/autobahn-python/tree/master/examples/asyncio/websocket/echo```
## Stream Rendering
For rendering the data, we use the WebGL Earth Library (```http://www.webglearth.org```) to render the edits on a map.
We specifically focus on a certain set of keys to be displayed, which are defined in ```config.json```. One may need to move around the map a little to see the edits. 

The background starfield effects were taken almost verbatim from the tutorial found at ```https://www.script-tutorials.com/night-sky-with-twinkling-stars/``` (minor edits were made to make it compatible with the WebGL library)

[1] https://github.com/hatnote/wikimon

------------------------------------------------
# Assignment 2

For this assignment, we've tried to make a rate alert using Redis and Amazon's SNS. The configurations for the analyze module is set in `config.py`. The system can be run with the simple command

```
python -u ws.py | process.py
```

To run the script to track the rate of stream, use
```
python analyze.py
```
------------------------------------------------
# Assignment 3

For this assigment, we built a snazzy dashboard to track the distribution of our messages.

The distribution would be defined on a set of binary variables such as 
1. Page Type (Special Page or Talk Page or Neither)
2. Is anonymous (true, false)

Therefore, we have 3*2 = 6 categories, and the distribution is essentially a *categorical* distribution.

## Running the Assignment
I have now set up a flask server for both the main display and the analytics dashboard.

To run the websocket, run
```
websocket --port 5000 python -u ws.py
```

To run the analytics server, run :

```
sudo python server.py
```
Note that the server needs to run as root, since the python system 
## Additional Categorical Variables?
We could obviously extend the analysis to include additional categories. The way code is laid out right now, it's extremely easy to add further discrete feature into the mix. Just go to `distribution.py` and we just have to set up a nice function to return a string based on the category, and make sure out `categorize_and_push_to_redis` function is aware of this function.

The system to build and maintain the dashboard is agnoistic to the number of categorical variables chosen. It will figure that out from the Redis Keys.

#### Adding more variables
As stated previously, just make a function that returns a different string for any categorical variable. But since Redis uses this string 'as-is' to render the dashboard, it would be helpful to use a descriptive string as 'is-bot' or 'is-not-bot'. Also. **PLEASE DO NOT INCLUDE SPACES OR UNDERSCORE IN THIS STRING**. Use hyphens instead of spaces.

## Stream Entropy Analysis

For a stream such as Wikipedia Edits, it's a worthwhile endeavour to build a notification system around the entropy of the distribution. Since the distribution is expected to be largely stable, it would be really useful to any irregularities, since that might show something really useful (such as vandalism or server error).

Also, Since the stream is largely unpredicatable (the stream edits form a markovian chain), the best way to predict the next message would be to use markovian chain analysis. Since no (trivial) ibrary supports Markvoian chains, I just decided to use the prior probabilities as the basis for choosing the next expected message.
