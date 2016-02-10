"""
Python script to pull data from the wikipedia edits websocket connection, filter it a bit, and 
return the json formatted string.
"""
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json

import config


class MyClientProtocol(WebSocketClientProtocol):
    """
    Client Protocol Class
    """
    def onConnect(self, response):
        if config.verbose:
            print("Server connected: {0}".format(response.peer))
        connect = True

    def onOpen(self):
        if config.verbose:
            print("WebSocket connection open.")
        ws_connect=True

    def onMessage(self, payload, isBinary):
        if isBinary:
            if config.verbose:
                print("Binary message received: {0} bytes".format(len(payload)))
            binary_message=True
        else:
            data = payload.decode('utf8')
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
                pass
            # print("{0}".format())

    def onClose(self, wasClean, code, reason):
        if config.verbose:
            print("WebSocket connection closed: {0}".format(reason))
        ws_connect = False


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    address_with_port = "{0}:{1}".format(config.SERVER_ADDRESS, config.SERVER_PORT)
    factory = WebSocketClientFactory(address_with_port, debug=False)
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, config.SERVER_ADDRESS, config.SERVER_PORT)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()