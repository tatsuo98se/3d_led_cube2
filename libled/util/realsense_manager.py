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
        self.realsense = realsense
        self.is_stop = False
        self.frame = None

    def run(self):
        while not self.is_stop:
            self.realsense.wait_for_frames()
            self.frame = self.realsense.frame()
        self.dev.stop()
        pyrs.stop()


    
    def stop(self):
        self.is_stop = True

    def get_data(self):
        return self.frame 

class RealsenseManager:
    _instance = None

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        logger.i("Collecting updates from realsense server...")
        self.socket.connect("tcp://localhost:5556")
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self.worker = FrameWorker(self)
        self.worker.start()
        
    def wait_for_frames(self):
        pass

    def frame(self):
        return recv_array(self.socket)
 
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
    def get_data(cls):
        if cls._instance is not None:
            return cls._instance.worker.get_data()
        else:
            return None


    @classmethod
    def stop(cls):
        if cls._instance is not None:
            cls._instance.__stop()
            cls._instance = None

    def __stop(self):
        self.worker.stop()
