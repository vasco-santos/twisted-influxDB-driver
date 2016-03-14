import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient
from twistedInfluxDB.Object import InfluxObject


log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
db = InfluxClient('http://localhost', 8086, 'example', log)

data = {
    'value': 151561651,
    'otherval': 56151561
}

infObj = InfluxObject("cpu_load_short", {}, data)


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
d.addCallback(db.write_points)
d.addCallbacks(inserted, failed)
d.addBoth(done)
d.callback(infObj)

reactor.run()
