"""
Python script to pull data from the wikipedia edits websocket connection, filter it a bit, and 
return the json formatted string.
"""
from ws4py.client.threadedclient import WebSocketClient
import json

import config


class MyClientProtocol(WebSocketClient):
    """
    Client Protocol Class
    """

    def opened(self):
        if config.verbose:
            print("Server connected")
        connect = True


    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        data = m.data
        try:
            x = json.loads(data)
            if x['page_title'][:5] != "Talk:" and x['page_title'][:9] != "Special:" and x['is_anon'] == True: # filter to remove non page edits and discussions
                nd = dict()
                for key in config.retain_keys: #retain only a subset of the keys
                    nd[key] = x[key]
                y = json.dumps(nd)
                print y
        except Exception as e:
            if config.verbose:
                print "JSON Decode Error in {0}".format(data)
            error = 1
            pass

if __name__ == '__main__':
    ws = MyClientProtocol(config.SERVER_HOST) # protocols=['http-only', 'chat']
    ws.connect()
    ws.run_forever()
