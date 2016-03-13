import io
import json
from StringIO import StringIO

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger
from twisted.web.client import Agent, FileBodyProducer
from twisted.web.http_headers import Headers

from TwistedInfluxDB import TwistedInfluxDBClient
from TwistedInfluxDB import InfluxObject


log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
db = TwistedInfluxDBClient('http://localhost', 8086, 'example', log)

data = {
    'value' : 151561651,
    'otherval': 56151561
}

infObj = InfluxObject("cpu_load_short", {}, data)
query = "SELECT * FROM cpu_load_short WHERE region='us-west'"

def inserted(response):
    print response
    return response

def failed(data):
    print "Failed"
    print data
    return data
    
def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
#d.addCallback(db.insert)
d.addCallback(db.query)
d.addCallbacks(inserted, failed)
d.addBoth(done)
#d.callback(infObj)
d.callback(query)

reactor.run()


