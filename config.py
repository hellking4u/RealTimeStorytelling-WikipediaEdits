#--------Verbosity---------
#NOTE : Disable to pipe to websocketd
verbose = False

#--------Server-Name-------
SERVER_HOST = "ws://wikimon.hatnote.com"
SERVER_PORT = 9000
retain_keys = ['page_title', 'url', 'geo_ip', 'summary', 'change_size']
SERVER_ADDRESS = "{0}:{1}".format(SERVER_HOST, SERVER_PORT)

ANALYZE_TIME = 60

LOW_RATE = 3
HIGH_RATE = 5