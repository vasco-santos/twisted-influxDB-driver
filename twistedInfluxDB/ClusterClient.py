# -*- coding: utf-8 -*-
"""
This module contains an asynchronous python cluster client for InfluxDB.
"""

import urllib

from StringIO import StringIO
from twisted.internet import defer, reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class InfluxClusterClient(object):
    """ Class responsible for keeping the connection data, as well as
    provide methods for interacting with the database.
    """

    def __init__(self, hosts):
        pass