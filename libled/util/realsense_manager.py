import time
import numpy as np
import cv2
import json
import time
import traceback
from time import sleep
from threading import Thread
from led_draw_util import *
import logger
import zmq
from zmq_util import *

class FrameWorker(Thread):

    def __init__(self, realsense):
        super(FrameWorker,self).__init__()
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        logger.i("Collecting updates from realsense server...")
        self.socket.connect("tcp://localhost:5501")
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

        self.is_stop = False
        self.frame = None

    def run(self):
        while not self.is_stop:
            self.frame = recv_array(self.socket)
        self.dev.stop()
    
    def stop(self):
        self.is_stop = True

    def get_data(self):
        return self.frame
                

class RealsenseManager:
    _instance = None

    def __init__(self):
        self.worker = FrameWorker(self)
        self.worker.start()
        
    @classmethod
    def init(cls):
        if cls._instance is None:
            try:
                cls._instance = cls()
                logger.i("initialize realsense is successfull.")
            except:
                logger.e("initialize realsense failed.:" + str(sys.exc_info()[0]))
                logger.e(traceback.format_exc())

        return cls._instance

    @classmethod
    def get_instance(cls):
        return RealsenseManager.init()

    @classmethod
    def get_data(cls):
        instance = RealsenseManager.get_instance()
        if instance is not None:
            return instance.worker.get_data()
        else:
            return None

    @classmethod
    def stop(cls):
        if cls._instance is not None:
            cls._instance.__stop()
            cls._instance = None

    def __stop(self):
        self.worker.stop()
