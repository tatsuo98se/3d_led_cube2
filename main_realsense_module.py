import time
import numpy as np
import cv2
import json
import time
import traceback
from time import sleep
from threading import Thread
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
from libled.util.led_draw_util import *
import zmq
import libled.util.logger
from libled.util.zmq_util import *

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5501")

dev = None

try:
    pyrs.start()
    dev = pyrs.Device()
    logger.i("initialize realsense is successfull.")
    dev.apply_ivcam_preset(0)
    dev.set_device_option(rs_option.RS_OPTION_F200_LASER_POWER, 15.0)
    while True:


        dev.wait_for_frames()
        d = dev.depth /256.0
        d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_BONE)
        scale = max(32.0/640, 16.0/480)
        scaled =  get_scled_rgb_image(d, scale, scale) 
        frame = resize2(scaled, (16, 32), (-4,0), [[0]*4])
        send_array(socket, frame)
except:
    logger.e("initialize realsense failed.:" + str(sys.exc_info()[0]))
    logger.e(traceback.format_exc())

finally:
    if dev is not None:
        dev.stop()
    pyrs.stop()
    if socket is not None:
        socket.close()
    if context is not None:
        context.term()
