from ..object.led_dot_obj import LedDotObject
from libled.util.color import Color
from ..led_canvas import LedCanvas
from libled.object.led_dot_obj import LedDotObject
from libled.object.led_ripple_obj import LedRippleObject
from libled.object.led_fill_obj import LedFillObject
from libled.object.led_random_ripple_obj import LedRandomRippleObject
from libled.led_canvas import LedCanvas
from libled.filter.led_canvs_filter import LedCanvasFilter
from libled.filter.led_test_canvas_filter import LedTestCanvasFilter
from libled.filter.led_wave_canvas_filter import LedWaveCanvasFilter
from libled.filter.led_hsv_canvas_filter import LedHsvCanvasFilter


def get_blocks_in_loop(orders, start):
    blocks = []
    for i in range(start, len(orders)):
        if str(orders[i]) == 'ctrl-1':
            return blocks

        blocks.append(orders[i])
    
    return blocks

def flatten_blocks(orders):
    flatten = []
    i = 0
    while i<len(orders):
        if orders[i] == 'ctrl-1':
            loop = get_blocks_in_loop(orders, i+1) 
            flatten.extend(loop * 3)
            i += len(loop) + 2
            continue

        flatten.append(orders[i])
        i += 1

    return flatten

DEFAULT_LIFETIME = 5

def create_object(block):
    if block == 'object-1':
        return LedFillObject(Color(1,0,0), DEFAULT_LIFETIME)
    elif block == 'object-2':
        return LedRandomRippleObject(DEFAULT_LIFETIME)

def create_filter(block, canvas):
    if block == 'filter-0':
        return canvas
    elif block == 'filter-1':
        return LedHsvCanvasFilter(canvas)
    elif block == 'filter-2':
        return LedWaveCanvasFilter(canvas)

def create_block(block, canvas):
    if str(block).startswith('object'):
        return create_object(block)
    elif str(block).startswith('filter'):
        return create_filter(block, canvas)



