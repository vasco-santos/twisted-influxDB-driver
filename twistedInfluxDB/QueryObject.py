# -*- coding: utf-8 -*-
"""
Query Object for InfluxDB query.
"""


class InfluxQueryObject(object):

    def __init__(self, measurement, fields=None, condition=None):
        """ Create an InfluxDB Query object for querying the DB.

        Arguments:
            measurement: the value measured over the time.
            fields: the fields to select over the queried data.
            condition: a filter condition to be applied to the queried data..
        """
        self.measurement = measurement
        self.fields = fields
        self.condition = condition

    def generate_query(self):
        """ Generate parameterizable query in order to avoid attacks.
        """
        query = 'SELECT {} FROM {}'.format('*' if self.fields is None else self.fields, self.measurement)
        if self.condition is not None:
            query += ' WHERE {}'.format(self.condition)
        return query
