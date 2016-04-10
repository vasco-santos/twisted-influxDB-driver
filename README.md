# InfluxDB Asynchronous Driver for Python Twisted

TwistedInfluxDB is a [twisted](https://github.com/twisted/twisted) client for communicating with [InfluxDB](https://influxdata.com/time-series-platform/influxdb/).

> InfluxDB is a time series database built from the ground up to handle high write and query loads. InfluxDB is meant to be used as a backing store for any use case involving large amounts of timestamped data, including DevOps monitoring, application metrics, IoT sensor data, and real-time analytics.

## Installation

For installing InfluxDB, run the following commands:

```
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

For installing Twisted, run the following commands:

```
pip install twisted
```

Tested using InfuxDB versions 0.10, 0.11 and 0.12.

## Documentation

Work in progress... (Sphinx based)

## Examples

This repository contains 3 twisted examples to exemplify how to use the developed API. It is also compatible with InfluxDB Clusters.

### Example 1 - testCreate.py

```
Create a new InfluxDB database.
```

### Example 2 - testInsert.py

```
Insert new data to a specific measure in an InfluxDB database.
```

### Example 3 - testQuery.py

```
Make a parameterizable query to an InfluxDB database.
```
