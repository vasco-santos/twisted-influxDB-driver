# -*- coding: utf-8 -*-
"""
Example of a InfluxDB database creation using TwistedInfluxDB Driver.
"""


import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient


# Logger to bind to the API.
log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
# Database client setup configurations.
db = InfluxClient('http://localhost', 8086, 'example', log)
# Database name Parameter.
dbname = 'newDBname'


# Success Callback
def created(response):
    print (response)
    return response


# Failed Callback
def failed(data):
    print ("Failed")
    print (data)
    return data


# Stop reactor
def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
d.addCallback(db.createDatabase)
d.addCallbacks(created, failed)
d.addBoth(done)
d.callback(dbname)

# Start Reactor
reactor.run()
