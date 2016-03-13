
class InfluxObject(object):
    def __init__(self, measurement, tags, data):
        self.measurement = measurement
        self.tags = tags
        self.data = data