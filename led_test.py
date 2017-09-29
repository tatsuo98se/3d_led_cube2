import base64
import cStringIO
from libled.led_cube import *
from libled.led_canvas import LedCanvas
from libled.object.led_dot_obj import LedDotObject
from libled.object.led_ripple_obj import LedRippleObject
from libled.object.led_fill_obj import LedFillObject
from libled.object.led_random_ripple_obj import LedRandomRippleObject
from libled.object.led_clear_obj import LedClearObject
from libled.object.led_bitmap_obj import LedBitmapObject

from libled.led_canvas import LedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from PIL import Image

mario0 = LedBitmapObject(Image.open('contents/s_mario.png'), 0, 10)
mario1 = LedBitmapObject(Image.open('contents/s_mario_run_1.png'), 0, 10)
mario3 = LedBitmapObject(Image.open('contents/s_mario_run_2.png'), 0, 10)
ripples =  LedRandomRippleObject(10)

canvas = LedCanvas()

canvas.add_object(ripples)
canvas.add_object(mario0)

while True:
    canvas.show()
    led.Wait(20)