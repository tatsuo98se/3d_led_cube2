from optparse import OptionParser
from libled.led_cube import *
from libled.util.led_block_util import *
import importlib
import os.path
from libled.util.color import Color
from libled.object.led_object import LedObject
from libled.object.led_dot_obj import LedDotObject
from libled.object.led_ripple_obj import LedRippleObject
from libled.object.led_fill_obj import LedFillObject
from libled.object.led_random_ripple_obj import LedRandomRippleObject
from libled.led_canvas import LedCanvas
from libled.i_led_canvas import ILedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter



parser = OptionParser()
parser.add_option("-d", "--dest",
                  action="store", type="string", dest="dest", 
                  help="(optional) ip address of destination device which connect to real 3d cube.")

(options, args) = parser.parse_args()

if options.dest != None:
    led.SetUrl(options.dest)


test_data = ["filter-2","object-2","object-1","object-2","object-1","filter-0","object-2","object-1"] # this line will be json
flatten_data = flatten_blocks(test_data)

#canvas = LedCanvas()
#canvas = LedHsvCanvasFilter(canvas)
#canvas = LedWaveCanvasFilter(canvas)

#canvas.add_object(LedDotObject(3, 3, 0, 0xffffff,5))
#canvas.add_object(LedRippleObject(3, 3, Color(0xff, 0xff, 0xff)))
#canvas.add_object(LedFillObject(Color(0xff, 0xff, 0xff)))
#canvas.add_object(LedRandomRippleObject(5))

base_canvas = LedCanvas()
canvas = base_canvas
current_block = None

for data in flatten_data:
    current_block = create_block(data, base_canvas)
    if isinstance(current_block, ILedCanvas):
        canvas = current_block
        continue
    else:
        canvas.add_object(current_block)

    while(True):
        assert isinstance(current_block, LedObject)
        if isinstance(current_block, LedObject) and current_block.is_expired():
            break

        canvas.show()
        led.Wait(20)



 