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

    def __init__(self, realsense, host):
        super(FrameWorker,self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        logger.i("Collecting updates from realsense server...:{0}".format(host))
        self.socket.connect("tcp://{0}:5501".format(host))
        self.socket.setsockopt(zmq.SUBSCRIBE, '')

        self.is_stop = False
        self.frame = None

    def run(self):
        try:
            while not self.is_stop:
                self.frame = recv_array(self.socket)
        finally:
            if self.socket is not None:
                self.socket.close()
            if self.context is not None:
                self.context.term()
    
    def stop(self):
        self.is_stop = True

    def get_data(self):
        return self.frame
                

class RealsenseManager:
    _instance = None

    def __init__(self, host):
        self.worker = FrameWorker(self, host)
        self.worker.start()
        
    @classmethod
    def init(cls, host):
        if cls._instance is None:
            cls._instance = cls(host)

        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

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
