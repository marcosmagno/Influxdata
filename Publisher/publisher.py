import logging
import asyncio
import random
import time
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2
import argparse

class Data(object):
    """This class is to gerate data.
            Attributes:
            choice_temperature (int): A number to represent the temperature.

    """

    def __init__(self):
        self.choice_temperature = 0

    def set_data(self):
        """Method for setting a random temperature with the random choice function.
            Attribute:
                temperature (list): An integer list.

        """

        temperature = [20, 21, 22, 23, 27, 30, 32]  # Vector of temperature
        self.choice_temperature = random.choice(temperature)

    def get_data(self):
        """Method to return a value of temperature
            return:
                choice_temperature (int): A value of temperature
        """

        return self.choice_temperature


class Publisher(object):
    """This class is to connect and publish values of temperature in MQTT server.
        Attribute:
            cliente (Object): An object that represent a connection with MQTT
            dataToSend (int): An integer representing a temperature.
            tasks (generator): An generator representing a task object.

    """

    def __init__(self, args):
        """ This constructor for Publisher """
        self.arg = args
        try:
            self.client = MQTTClient()
        except Exception as e:
            print(e)

    @asyncio.coroutine
    def send_mqtt(self, data):
        """This method is responsible to connect on client   and publish temperature values.
            Parameter:
                data (int): Value of temperature

         """
        self.dataToSend = data

        try:
            yield from self.client.connect('mqtt://' + str(self.arg.server_ip))            
            tasks = [asyncio.ensure_future(self.client.publish(self.arg.topic, bytes(str(self.dataToSend), 'utf-8')))]

            yield from asyncio.wait(tasks)

            # Disconnects the client when finished.
            yield from self.client.disconnect()
        except Exception as e:
            print(e)

    def run(self, recv_generator):
        """This method is responsible to start the process.
            Parameter:
                recv_generator (generator): An generator of connection and publish.

         """
        asyncio.get_event_loop().run_until_complete(recv_generator)


def main():
    """This class is responsible to start the program.
            Attribute:
                    obj_Data (Object): An object of class Data.
                    obj_Publisher (Object): An object of class Publisher
    """

    parser = argparse.ArgumentParser(
        description='Subscribe to MQTT server')

    parser.add_argument('--server_ip', type=str, required=False,
                        default='127.0.0.1', help='IP of MQQT server')

    parser.add_argument('--topic', type=str, required=False,
                        default='sensor/temperature', help='Topic filters to subscribe.')

    obj_Data = Data()
    obj_Publisher = Publisher(parser.parse_args())

    while True:
        obj_Data.set_data()
        # time.sleep(0.2)
        obj_Publisher.run(obj_Publisher.send_mqtt(obj_Data.get_data()))


if __name__ == '__main__':
    main()
