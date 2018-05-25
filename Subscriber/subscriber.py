import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


@asyncio.coroutine
def recv_mqtt():

    C = MQTTClient()
    yield from C.connect('mqtt://192.168.0.16')

    yield from C.subscribe([
        ('a/b', QOS_1)

    ])
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d:  %s => %s" % (
                i, packet.variable_header.topic_name, str(packet.payload.data)))

        yield from C.unsubscribe(['a/b'])
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(recv_mqtt())
