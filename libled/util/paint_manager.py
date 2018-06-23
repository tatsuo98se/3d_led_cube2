import time
import numpy as np
import cv2
import json
import time
import traceback
import color
from led_draw_util import *
import logger

class PaintManager:
    _instance = None

    def __init__(self):
        self._canvas = [[Color(0,0,0,0) for height in range(LED_HEIGHT)] for width in range(LED_WIDTH)]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                cls._instance = cls()
                logger.i("initialize paint manager is successfull.")
            except:
                logger.e("initialize paint manager failed.:" + str(sys.exc_info()[0]))
                logger.e(traceback.format_exc())

        return cls._instance

    def get_data(self):
        return self._canvas

    def get_color(self, x, y):
        return self._canvas[x][y]

    def set_color(self, x, y, color):
        self._canvas[x][y] = color

