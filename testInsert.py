# -*- coding: utf-8 -*-
"""
Example of a InfluxDB insertion using TwistedInfluxDB Driver.
"""


import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient
from twistedInfluxDB.Object import InfluxObject


# Logger to bind to the API.
log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
# Database client setup configurations.
db = InfluxClient('http://localhost', 8086, 'example', log)
# Data to be inserted to cpu_load_short measure
data = {
    'value': 151561651,
    'otherval': 56151561
}
# Insertion parameter (Influx Object)
infObj = InfluxObject("cpu_load_short", {}, data)


# Success Callback
def inserted(response):
    print (response)
    return response


# Failed Callback
def failed(exception):
    print "Failed"
    print (exception)
    return exception


# Stop reactor
def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
d.addCallback(db.write_points)
d.addCallbacks(inserted, failed)
d.addBoth(done)
d.callback(infObj)

# Start Reactor
reactor.run()
