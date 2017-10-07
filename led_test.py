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
from libled.object.led_mario_jump_obj import LedMarioJumpObject
from libled.object.led_mario_run_obj import LedMarioRunObject
from libled.object.led_mario_runjump_obj import LedMarioRunJumpObject
from libled.object.led_drop_mushroom_obj import LedDropMushroomObject

from libled.led_canvas import LedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from PIL import Image

mario0 = LedBitmapObject(Image.open('asset/image/s_mario.png'), 0, 0, 0, 10)
mario1 = LedBitmapObject(Image.open('asset/image/s_mario_run_1.png'), 0, 0, 0, 10)
mario3 = LedBitmapObject(Image.open('asset/image/s_mario_run_2.png'), 0, 0, 0, 10)
marioj = LedMarioJumpObject(0, 0, 10)
mariorj = LedMarioRunJumpObject(0, 0, 10)
mashroom = LedDropMushroomObject(0)
ripples =  LedRandomRippleObject(10)
mario_run = LedMarioRunObject(0, 10)

canvas = LedCanvas()

canvas.add_object(ripples)
#canvas.add_object(mario_run)

while True:
    canvas.show()
    led.Wait(20)