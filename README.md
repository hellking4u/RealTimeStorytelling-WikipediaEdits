# RealTimeStorytelling-WikipediaEdits
A map showing anonymous edits made to Wikipedia in real time.

## Stream Description
The aim of the project was to try and map out geolocatable wikipedia edits in real time. Fortunately, *Wikipedia* publishes it's recent changes in an IRC feed (details of which can be found here : ```https://meta.wikimedia.org/wiki/IRC/Channels#Wikipedia```). This saves a tremendous amount of time as we need not poll the service. To make our lives easier still, a github user **hatnote** has create a repo to consume this IRC feed and create a public websocket URL to consume. The repo can be found here : ```https://github.com/hatnote/wikimon```.

The websocket stream has a JSON like description, with multiple required fields.

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

## Stream Processing
We use the *Wikimon* websocket connection to recieve real-time edits. We filter the data which is actually a 'Page' edit and not an edit on the 'Talk' page or 'Special' page. We consequently filter on anonymous edits as they contain the geolocation of the editor. While tracking registered edits might be feasible, it would entail significantly more probing. Limiting tracking to anonymous edits means we tap into approximately 15% of the total stream, but it also makes the stream a more manageable size, with about 1 edit per second.

The stream is handled using Python using the Autobahn (asyncio) library. The code to recieve messages on a websocket stream is partly taken from the Autobahn Example 'echo'. ```https://github.com/crossbario/autobahn-python/tree/master/examples/asyncio/websocket/echo```
## Stream Rendering
For rendering the data, we use the WebGL Earth Library (```http://www.webglearth.org```) to render the edits on a map.
We specifically focus on a certain set of keys to be displayed, which are defined in ```config.json```. One may need to move around the map a little to see the edits. 

The background starfield effects were taken almost verbatim from the tutorial found at ```https://www.script-tutorials.com/night-sky-with-twinkling-stars/``` (minor edits were made to make it compatible with the WebGL library)