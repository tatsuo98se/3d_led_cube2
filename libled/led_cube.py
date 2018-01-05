import os
from ctypes import *
import sys
import platform

LED_HEIGHT = 32
LED_WIDTH = 16
LED_DEPTH = 8

dirname = os.path.dirname(__file__)
if sys.platform == 'darwin':
    ledlib = dirname + '/libledLib.dylib'
elif sys.platform == 'win32':
    arch = platform.architecture()[0]
    if arch == '64bit':
        ledlib = dirname + '/ledLib64.dll'
    else:
        ledlib = dirname + '/ledLib32.dll'
<<<<<<< HEAD
elif 'linux' in sys.platform and platform.machine() == 'armv7l':
    ledlib = dirname + '/ledLibarmv7l.so' # for Raspberry PI3
=======
elif 'linux' in sys.platform:
    ledlib = dirname + '/ledLib.so' # build for raspberry pi
>>>>>>> 11cec0e698eb7d5ee338551ce8c61d1ab5014cf4
else:
    raise NotImplementedError('Unsupported OS.' + sys.platform)

print('LoadLibrary: '+ ledlib)


class LedCube(object):
    def __init__(self, led):
        self.led = led

    def Show(self):
        #print("led.Show()")
        self.led.Show()

    def SetUrl(self, dest):
        #print("led.SetUrl()")
        self.led.SetUrl(dest)

    def Clear(self):
        #print("led.Clear()")
        self.led.Clear()
    
    def SetLed(self, x, y, z, color):
        # print("led.SetLed()") comment out for performance
        self.led.SetLed(x, y, z, color)
    
    def Wait(self, msec):
        self.led.Wait(int(msec))

    def EnableSimulator(self, is_enable):
        self.led.EnableSimulator(is_enable)

led = LedCube(cdll.LoadLibrary(ledlib))
