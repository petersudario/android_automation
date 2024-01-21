import os
import configparser
import time


class Controller:

    def __init__(self, device, device_number):
        self.device = device
        self.device_number = device_number

    def perform_movement(self, movement):
        config = configparser.ConfigParser()
        config.read("controller.conf")

        direction = config.get("controller", movement)
        os.system(direction)
        print("Moving ", movement)
        time.sleep(2)


