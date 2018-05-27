'''
curl -i -XPOST 'http://localhost:8086/write?db=virturian' --data-binary 'temperature,node=node1 value=22'
'''
# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse

from influxdb import InfluxDBClient


def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'
    dbname = 'virturian'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select value from temperature;'

    json_body = [
        {
            "measurement": "temperature",
            "fields": {
                "node":"d",
                "value": 4
                
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    result = client.query(query)

    print("Result: {0}".format(result))
    client.drop_database(dbname)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)