import time
import numpy as np
import cv2
import json
import time
from time import sleep
from threading import Thread
import pyrealsense as pyrs
import realsense_manager_impl
from led_draw_util import *
import logger

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
        pyrs.start()
        self.dev = pyrs.Device()
        self.dev.apply_ivcam_preset(0)
        self.dev.set_device_option(rs_option.RS_OPTION_F200_LASER_POWER, 15.0)
        self.worker = FrameWorker(self)
        self.worker.start()

    def wait_for_frames(self):
        self.dev.wait_for_frames()

    def frame(self):
        # put red light top 
#        d = self.dev.depth * self.dev.depth_scale * 1000
        d = self.dev.depth /256.0
        d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_BONE)
#        d = np.rot90(d)
        scale = max(32.0/480, 16.0/640)
        scaled =  get_scled_rgb_image(d, scale, scale) # / 256.0
        return resize2(scaled, (16, 32), (0,0), [[0]*4])
 
    @classmethod
    def init(cls):
        if cls._instance is None:
            try:
                cls._instance = cls()
                logger.i("initialize realsense is successfull.")
            except:
                logger.e("initialize realsense failed.:" + str(sys.exc_info()[0]))

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
