import io

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.logger import jsonFileLogObserver, Logger

from twistedInfluxDB.Client import InfluxClient


log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")))
db = InfluxClient('http://localhost', 8086, 'example', log)

dbname = 'newDBname'


def created(response):
    print (response)
    return response


def failed(data):
    print ("Failed")
    print (data)
    return data


def done(_):
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()
d.addCallback(db.createDatabase)
d.addCallbacks(created, failed)
d.addBoth(done)
d.callback(dbname)

reactor.run()
