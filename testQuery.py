# -*- coding: utf-8 -*-
"""
Example of a InfluxDB query using TwistedInfluxDB Driver.
"""


import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient
from twistedInfluxDB.QueryObject import InfluxQueryObject


# Logger to bind to the API.
log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
# Database client setup configurations.
db = InfluxClient('http://localhost', 8086, 'example', log)
# Query Parameter (Influx Query Object)
query = InfluxQueryObject('cpu_load_short', fields=None, condition="region='us-west'")


# Success Callback
def inserted(response):
    print (response)
    return response


# Failed Callback
def failed(data):
    print "Failed"
    print (data)
    return data


# Stop reactor
def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
d.addCallback(db.query)
d.addCallbacks(inserted, failed)
d.addBoth(done)
d.callback(query)

# Start Reactor
reactor.run()
