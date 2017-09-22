from optparse import OptionParser
from libled.led_cube import *
import importlib
import os.path
from libled.led_dot_obj import LedDotObject
from libled.led_canvas import LedCanvas
from libled.led_test_canvas_filter import LedTestCanvasFilter

parser = OptionParser()
parser.add_option("-d", "--dest",
                  action="store", type="string", dest="dest", 
                  help="(optional) ip address of destination device which connect to real 3d cube.")

(options, args) = parser.parse_args()

if options.dest != None:
    led.SetUrl(options.dest)

canvas = LedTestCanvasFilter(LedCanvas())

canvas.add_object(LedDotObject(3, 3, 0, 0xffffff,5))

while(True):
    canvas.show()
    led.Wait(10)
