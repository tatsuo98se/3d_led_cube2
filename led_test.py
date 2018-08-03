# -*- encoding:utf8 -*-
import base64
import cStringIO
from libled.led_cube import *
from optparse import OptionParser
from libled.util.color import Color
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
from libled.object.led_snows_obj import LedSnowsObject, LedSnowObject
from libled.object.led_wave_obj import LedWaveObject
from libled.object.led_scrolled_bitmap_obj import LedScrolledBitmapObject
from libled.object.led_star_obj import LedStarObject
from libled.object.led_leafs_obj import LedLeafsObject
from libled.object.led_tree_obj import LedTreeObject


from libled.led_canvas import LedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from libled.filter.led_jump_canvas_filter import LedJumpCanvasFilter
from libled.filter.led_skewed_canvas_filter import LedSkewedCanvasFilter
from libled.filter.led_color_canvas_filter import LedColorCanvasFilter
from libled.filter.led_rainbow_canvas_filter import LedRainbowCanvasFilter
from libled.filter.led_random_color_canvas_filter import LedRandomColorCanvasFilter
from libled.filter.led_heartbeats_canvas_filter import LedHeartsBeatsCanvasFilter
from libled.filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter

mario0 = LedBitmapObject('asset/image/mario.png', 0, 0, 0, 1, 10)
mario1 = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, 0, 1, 10)
mario3 = LedBitmapObject('asset/image/mario_run_2.png', 0, 0, 0, 1, 10)
mario4 = LedBitmapObject('asset/image/mario_jump.png', 0, 0, 0, 1, 10)
star = LedBitmapObject('asset/image/star.png', 0, 0, 0, 1, 10)
skewed_sphere = LedSkewedSphereObject(10)
marioj = LedMarioJumpObject(0, 0, 10)
mariorj = LedMarioRunJumpObject(0, 0, 10)
mashroom = LedDropMushroomObject(0)
ripples =  LedRandomRippleObject(10)
mario_run = LedMarioRunObject(0, 10)
heart = LedHeartObject(10)
snow = LedSnowObject(10)
snows = LedSnowsObject(10)
cloud = LedWaveObject(range(-5, 4), int(0x888888) ,10)
wave = LedWaveObject(range(28, 36), int(0x0000ff) ,10)
bkgrass = LedScrolledBitmapObject('asset/image/background_grass.png', 0, 0, 7, 20)
bkmountain = LedScrolledBitmapObject('asset/image/background_mountain.png', 0, 0, 6, 20)
bkcloud = LedScrolledBitmapObject('asset/image/background_cloud.png', 0, 0, 7, 20)
mario_scr = LedScrolledBitmapObject('asset/image/mario.png', 0, 0, 0, 10)
star_3d = LedStarObject(10)
leafs = LedLeafsObject(int(0xffcccc), 30)
tree = LedTreeObject(False, 10)

canvas = LedCanvas()
#canvas = LedJumpCanvasFilter(canvas)
#canvas = LedSkewedCanvasFilter(canvas)
#canvas = LedColorCanvasFilter(canvas, int(0xff3333))
#canvas = LedRainbowCanvasFilter(canvas)
#canvas = LedHeartsBeatsCanvasFilter(canvas)
#canvas = LedRandomColorCanvasFilter(canvas)
canvas = LedSnowsObjectCanvasFilter(canvas)

#canvas.add_object(snows)
canvas.add_object(tree)
#canvas.add_object(bkcloud)
#canvas.add_object(bkgrass)

parser = OptionParser()
parser.add_option("-d", "--dest",
                        action="store", type="string", dest="dest", 
                        help="(optional) ip address of destination device which connect to real 3d cube.")

options, _ = parser.parse_args()
led = LedCubeFactory.get_instance()

if options.dest != None:
    print("External Connect To: " + (options.dest))
    led.SetUrl(options.dest)

while True:
    canvas.show()
    led.Wait(20)