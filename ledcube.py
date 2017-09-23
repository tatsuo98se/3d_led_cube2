from optparse import OptionParser
from libled.led_cube import *
import importlib
import os.path
from libled.util.color import Color
from libled.object.led_dot_obj import LedDotObject
from libled.object.led_ripple_obj import LedRippleObject
from libled.led_canvas import LedCanvas
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter



parser = OptionParser()
parser.add_option("-d", "--dest",
                  action="store", type="string", dest="dest", 
                  help="(optional) ip address of destination device which connect to real 3d cube.")

(options, args) = parser.parse_args()

if options.dest != None:
    led.SetUrl(options.dest)


test_data = ["filter-1","object-1"]

for data in test_data:
    pass

canvas = LedWaveCanvasFilter(LedCanvas())

#canvas.add_object(LedDotObject(3, 3, 0, 0xffffff,5))
canvas.add_object(LedRippleObject(3, 3, Color(0xff, 0xff, 0xff)))

while(True):
    canvas.show()
    led.Wait(10)
