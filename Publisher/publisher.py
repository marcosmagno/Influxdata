import logging
import asyncio
import random
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2

def generate_data():
    temperature = [20,21,22,23,27,30,32]
    choice_temperature = random.choice(temperature)
    return choice_temperature
    


@asyncio.coroutine
def send_mqtt():
    t = generate_data()
    print("tttt", t)
    print(type(t))

    C = MQTTClient()
    yield from C.connect('mqtt://192.168.0.16')    
    tasks = [asyncio.ensure_future(C.publish('a/b', bytes(str(t), 'utf-8')))
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()





if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(send_mqtt())
    
