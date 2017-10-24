# -*- encoding:utf8 -*-
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
from libled.object.led_text_obj import LedTextObject
from libled.object.led_heart_obj import LedHeartObject
from libled.object.led_skewed_sphere_obj import LedSkewedSphereObject

from libled.led_canvas import LedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from libled.filter.led_jump_canvas_filter import LedJumpCanvasFilter
from libled.filter.led_skewed_canvas_filter import LedSkewedCanvasFilter

mario0 = LedBitmapObject('asset/image/mario.png', 0, 0, 0, 10)
mario1 = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, 0, 10)
mario3 = LedBitmapObject('asset/image/mario_run_2.png', 0, 0, 0, 10)
mario4 = LedBitmapObject('asset/image/mario_jump.png', 0, 0, 0, 10)
star = LedBitmapObject('asset/image/star.png', 0, 0, 0, 10)
skewed_sphere = LedSkewedSphereObject(10)
marioj = LedMarioJumpObject(0, 0, 10)
mariorj = LedMarioRunJumpObject(0, 0, 10)
mashroom = LedDropMushroomObject(0)
ripples =  LedRandomRippleObject(10)
mario_run = LedMarioRunObject(0, 10)
heart = LedHeartObject(10)

canvas = LedCanvas()
canvas = LedJumpCanvasFilter(canvas)
#canvas = LedSkewedCanvasFilter(canvas)

canvas.add_object(mario_run)
#canvas.add_object(mario_run)

while True:
    canvas.show()
    led.Wait(20)