

import urllib

from StringIO import StringIO
from twisted.internet import defer, reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class InfluxClient(object):
    
    def __init__(self, host, port, database, log):
        self.client = host + ':' + str(port)
        self.database = database
        self.log = log
        
    def write_points(self, data):
        
        def cbRequest(response):
            self.log.info("Insert RES:     Code: {} - Headers: {}".format(str(response.code),
                    ''.join(str(e) for e in response.headers.getAllRawHeaders())))
            return response.code
        
        # Start Client Agent
        agent = Agent(reactor)
        
        # Body Format measurement,[tags] [fields]
        format = '' if data.tags == {} else ','
        body = (data.measurement + format +
                ','.join(['{}={}'.format(k,v) for k,v in data.tags.iteritems()]) +
                ' ' + ','.join(['{}={}'.format(k,v) for k,v in data.data.iteritems()]))
        
        # Rest Method
        d = agent.request(
            'POST',
            self.client + '/write?db=' + self.database,
            Headers({'User-Agent': ['Twisted InfluxDB Client'],
                    'Content-Type': ['text/x-greeting']}),
            FileBodyProducer(StringIO(body)))
        d.addCallback(cbRequest)
        
        self.log.info("Insert REQ:     {} - Body: {}".format(self.client, body))
        return d
        
        
    """
    
    
    """
    def query(self, query):
        
        def cbRequest(response):
            self.log.info("Query RES:     Code: {} - Headers: {}".format(str(response.code),
                    ''.join(str(e) for e in response.headers.getAllRawHeaders())))
            d = readBody(response)
            return d
            
        # Start Client Agent
        agent = Agent(reactor)

        body = {
            'db': self.database,
            'q': query
        }
        
        # Rest Method
        d = agent.request(
            'GET',
            #client,
            self.client + '/query?pretty=true&' + urllib.urlencode(body),
            Headers({'User-Agent': ['Twisted InfluxDB Client'],
                    'Content-Type': ['application/x-www-form-urlencoded']}),
            None)
        d.addCallback(cbRequest)
        
        self.log.info("Query REQ:     {} - Query: {}".format(self.client, query))
        return d

    
    """
    
    """
    def create_database(self, name):
        pass