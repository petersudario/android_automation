import os
import time


class Control(object):

    def swipe(self, direction):
        os.system(direction)
        time.sleep(2)