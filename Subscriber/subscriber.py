import logging
import asyncio
import argparse
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from influxdb import InfluxDBClient
import time


class Subscribe(object):
    """docstring for Subscribe"""

    def __init__(self, args):
        self.arg = args
        print(self.arg.server_ip)
        self.db = InfluxDB()

    @asyncio.coroutine
    def recv_mqtt(self):

        C = MQTTClient()
        yield from C.connect('mqtt://' + str(self.arg.server_ip))

        yield from C.subscribe([
            (self.arg.topic, QOS_1)

        ])
        try:
            while True:
                message = yield from C.deliver_message()
                packet = message.publish_packet
                print("%s" % (str(packet.payload.data).split("'")[1]))
                v = str(packet.payload.data).split("'")[1]
                self.db.writeDB("node1", int(v))

            yield from C.unsubscribe([self.arg.topic])
            yield from C.disconnect()
        except ClientException as ce:
            logger.error("Client exception: %s" % ce)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.recv_mqtt())


class InfluxDB(object):
    """docstring for ClassName"""

    def __init__(self):
        """Instantiate a connection to the InfluxDB."""
        self.user = 'root'
        self.password = 'root'
        self.dbname = 'virturian'

        self.host = "localhost"
        self.port = 8086

        self.client = InfluxDBClient(
            self.host, self.port, self.user, self.password, self.dbname)

    def writeDB(self, node, temperature):
        


        json_value = [
            {
                "measurement": "temperature",
                "fields": {
                    "node": 1,
                    "value": int(temperature)

                }
            }
        ]

        self.client.write_points(json_value)


def main():
    parser = argparse.ArgumentParser(
        description='Subscribe to MQTT server')

    parser.add_argument('--server_ip', type=str, required=False,
                        default='192.168.0.16', help='IP of MQQT server')

    parser.add_argument('--topic', type=str, required=False,
                        default='sensor/temperature', help='Topic filters to subscribe.')

    objSubscribe = Subscribe(parser.parse_args())
    objSubscribe.run()

    #objSubscribe = Subscribe(host=args.host, topic=args.topic)

if __name__ == '__main__':
    main()
