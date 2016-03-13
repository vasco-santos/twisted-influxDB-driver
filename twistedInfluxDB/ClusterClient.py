

import urllib

from StringIO import StringIO
from twisted.internet import defer, reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class InfluxClient(object):

    def __init__(self, hosts):
        pass