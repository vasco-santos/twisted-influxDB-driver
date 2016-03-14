# -*- coding: utf-8 -*-
"""
Object for InfluxDB insertion.
"""


class InfluxObject(object):

    def __init__(self, measurement, tags, data):
        """ Create an InfluxDB object for inserting in the DB.

        Arguments:
            measurement: the value to measure over the time.
            tags: the tags associated with the measure.
            data: the measured value at the inserted time.
        """
        self.measurement = measurement
        self.tags = tags
        self.data = data
