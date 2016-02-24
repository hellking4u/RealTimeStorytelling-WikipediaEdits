"""
Python script to pull data from the wikipedia edits websocket connection, filter it a bit, and 
return the json formatted string.

It pulls data from a WebSocket server that sends out JSON messages as string. It parses that data
and prints it out on stdout
"""
from ws4py.client.threadedclient import WebSocketClient # changed from autobahn to ws4py
import json

# The config file defines configuratiosn that are not part of the code logic. It includes settings
# such as the analyze time, verbosity, and the server addresses.
import config 


class MyClientProtocol(WebSocketClient):
    """
    Client Protocol Class. Implements the 3 functions to handle opening, closing and the message event
    on the stream.
    """

    def opened(self):
        """
        This is the function called when a WebScoket stream is opened. It looks at the verbosity 
        setting defined in config and prints out a diagnostic message accordingly.
        """
        if config.verbose:
            print("Server connected")

    def closed(self, code, reason=None):
        """
        This is the function called when a WebScoket stream is closed. It looks at the verbosity 
        setting defined in config and prints out a diagnostic message with the return code and the 
        reason for closure.
        """
        if config.verbose:
            print "Closed down", code, reason

    def received_message(self, m):
        """
        The received_message function takes an argument 'm' (of ws4py's message class) and prints out a parsed JSON on stdout.
        """
        # unpacking the data that was in the ws4py.TextMessage type.

        data = m.data

        # We wrap our logic in a try-except block because we do not want the code to exit in case of a erratic message recieved or
        # a random JSON decode error. There is a known case of JSON decode error on special Edit pages which we can safely ignore,
        # since they are not part of the data we are wishing to capture in this scope.
        try:
            x = json.loads(data)
            if x['page_title'][:5] != "Talk:" and x['page_title'][:9] != "Special:" and x['is_anon'] == True: # filter to remove non page edits and discussions
                nd = dict()
                #retain only a subset of the keys that we are interested in. These keys are defined in the config file
                for key in config.retain_keys: 
                    nd[key] = x[key]
                print json.dumps(nd)
        except Exception as e:
            if config.verbose:
                print "JSON Decode Error in {0}".format(data)
            pass

if __name__ == '__main__':
    # set up websocket connection to the server host defined in config.
    ws = MyClientProtocol(config.SERVER_HOST)
    # connect to the server and run the recieve hook continuously
    ws.connect()
    ws.run_forever()
