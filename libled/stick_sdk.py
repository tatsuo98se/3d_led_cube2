import os
from ctypes import *
import sys
import platform
import util.logger as logger
from PIL import Image
from datetime import datetime

dirname = os.path.dirname(__file__)
lib = os.path.abspath(os.path.join(dirname, 'libsticksdk.so'))

#logger.i('LoadLibrary: '+ str(ledlib))

class LedStick(object):

    def __init__(self, stick):
        self.stick = stick

    def init_sdk(self):
        self.stick.init_sdk()

    def stop_led_demo(self):
        self.stick.stop_led_demo()

    def _get_led_rgb(self, c):
        r = (c & 0xff0000) >> 16
        g = (c & 0x00ff00) >> 8
        b = (c & 0x0000ff)
        return int(round(r/85.0)),\
                int(round(g/85)),\
                int(round(b/85))
    
    def _flatten_pattern(self, pattern):
        flat = []
        for p in pattern:
            flat.extend(self._get_led_rgb(p))
        return flat

    def write_line(self, line, pattern):
        faltten = self._flatten_pattern(pattern)
        carray = c_byte * len(faltten) 
        cpattern = carray(*faltten) 
        self.stick.write_line(line, cpattern)

    def show_line(self, line):
        self.stick.show_line(line)

    def get_accel(self):
        carray = c_short * 3
        s_arr = [0 for _ in range(3)]  
        a = carray(*s_arr)  
        self.stick.get_accel(a)
        return (a[0],a[1],a[2])

    def get_gyro(self):
        carray = c_short * 3
        s_arr = [0 for _ in range(3)]  
        g = carray(*s_arr)  
        self.stick.get_gyro(g)
        return (g[0],g[1],g[2])

class LedStickDummy(LedStick):
    def __init__(self):
        pass

    def init_sdk(self):
        pass

    def stop_led_demo(self):
        pass

    def write_line(self, line, pattern):
        faltten = self._flatten_pattern(pattern)
        carray = c_byte * len(faltten) 
        cpattern = carray(*faltten)
        logger.i('write_line:' + str(line))
        pass

    def show_line(self, line):
        pass

    def get_accel(self):
        return [0,0,0]

    def get_gyro(self):
        return [0,0,0]

def create_led_stick(lib):
    try:
        return LedStick(cdll.LoadLibrary(lib))
    except OSError:
        return LedStickDummy()

STICK = create_led_stick(lib)
