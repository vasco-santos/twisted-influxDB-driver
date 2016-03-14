import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient


log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
db = InfluxClient('http://localhost', 8086, 'example', log)


query = "SELECT * FROM cpu_load_short WHERE region='us-west'"


def inserted(response):
    print (response)
    return response


def failed(data):
    print "Failed"
    print (data)
    return data


def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
d.addCallback(db.query)
d.addCallbacks(inserted, failed)
d.addBoth(done)
d.callback(query)

#count = 0
#while (count < 20):
#    print "hello"
#    count+=1

reactor.run()

