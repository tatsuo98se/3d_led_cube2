import time
import numpy as np
import cv2
import json
import time
import traceback
import color
from led_draw_util import *
import logger
import sync

class PaintManager:
    _instance = None
    _lock = sync.create_lock()

    def __init__(self):
        self._canvas = [[Color(0,0,0,0) for _ in range(LED_HEIGHT)] for _ in range(LED_WIDTH)]

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

    @sync.synchronized(_lock)
    def get_data(self):
        return self._canvas

    @sync.synchronized(_lock)
    def get_color(self, x, y):
        return self._canvas[x][y]

    @sync.synchronized(_lock)
    def set_color(self, x, y, color):
        self._canvas[x][y] = color

