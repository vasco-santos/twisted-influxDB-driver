# -*- coding: utf-8 -*-
"""
This module contains an asynchronous python client for InfluxDB.
"""

import urllib

from StringIO import StringIO
from twisted.internet import reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class InfluxClient(object):
    """ Class responsible for keeping the connection data, as well as
    provide methods for interacting with the database.
    """

    def __init__(self, host, port, database, log):
        """ Create a client for InfluxDB communication.

        Arguments:
            host: the url of the database.
            port: the port to communicate with the database.
            database: name of the database to use.
            log: the twisted log instance.
        """
        self.client = host + ':' + str(port)
        self.database = database
        self.log = log
        
    def write_points(self, data):
        """ Insert data new data in the Database.

        Arguments:
            data: InfluxDB Object composed by measurement, tags and data.

        Returns:
            the code of the InfluxDB HTTP response.
        """

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
        
    def query(self, query):
        """ Get data from the database.

        Arguments:
            query: the SQL-like query to be dispatched to the database.

        Returns:
            the result received by the Database (HTTP response body).
        """

        def cbRequest(response):
            self.log.info("Query RES:     Code: {} - Headers: {}".format(str(response.code),
                    ''.join(str(e) for e in response.headers.getAllRawHeaders())))
            #d = readBody(response)
            #return d
            return readBody(response)
            
        # Start Client Agent
        agent = Agent(reactor)

        # Rest Method
        params = {
            'db': self.database,
            'q': query.generate_query()
        }
        d = agent.request(
            'GET',
            self.client + '/query?pretty=true&' + urllib.urlencode(params),
            Headers({'User-Agent': ['Twisted InfluxDB Client'],
                    'Content-Type': ['application/x-www-form-urlencoded']}),
            None)
        d.addCallback(cbRequest)
        
        self.log.info("Query REQ:     {} - Query: {}".format(self.client, query))
        return d

    def createDatabase(self, name):
        """ Create a InfluxDB database.

        Arguments:
            name: database intended name.

        Returns:
            the code of the InfluxDB HTTP response.
        """
        def cbRequest(response):
            self.log.info("Create RES:     Code: {} - Headers: {}".format(str(response.code),
                    ''.join(str(e) for e in response.headers.getAllRawHeaders())))
            return response.code

        # Start Client Agent
        agent = Agent(reactor)

        # Rest Method
        params = {
            'q': "CREATE DATABASE " + name
        }

        d = agent.request(
            'GET',
            self.client + '/query?' + urllib.urlencode(params),
            Headers({'User-Agent': ['Twisted InfluxDB Client'],
                    'Content-Type': ['application/x-www-form-urlencoded']}),
            None)
        d.addCallback(cbRequest)

        self.log.info("Create REQ:     {} - Query: {}".format(self.client, name))
        return d
