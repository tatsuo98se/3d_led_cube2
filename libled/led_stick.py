import os
from ctypes import *
import sys
import platform
import util.logger as logger
import time
from PIL import Image
from datetime import datetime
from libled.util.color import Color
import numpy as np
import util.logger
import traceback
from stick_sdk import STICK
from threading import Thread

LED_HEIGHT = 32
LED_WIDTH = 16
LED_DEPTH = 8


class LedStickCube(object):
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._unique_instance = cls()

        return cls._unique_instance

    def __init__(self):
        self.stick = STICK
        self.stick.init_sdk()
        self.__init_image()

    def __init_image(self):
        self.canvas_history = np.ndarray((LED_WIDTH, LED_HEIGHT), dtype='int16')
        self.image = np.ndarray((LED_WIDTH, LED_HEIGHT), dtype='int32')
        self.image.fill(0)
        self.__clear_history()

    def __clear_history(self):
        self.canvas_history.fill(LED_DEPTH)

    def Show(self):
        for x in range(LED_WIDTH):
            line = self.image[x,:]
            self.stick.write_line(x, line)

        self.__clear_history()

    def SetUrl(self, dest):
        print("led.SetUrl():" + dest)

    def Clear(self):
        #print("led.Clear()")
        self.__init_image()
    
    def SetLed(self, x, y, z, color):
        zhistory = self.canvas_history[x,y]
        if zhistory < z:
            return
        self.canvas_history[x,y] = z
        self.image[x,y] = Color.rgbint_to_bgrint(color)
    
    def Wait(self, msec):
        time.sleep(msec/1000.0)

    def EnableSimulator(self, is_enable):
        pass

    def Stop(self):
        pass
