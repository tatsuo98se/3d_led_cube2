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
        if str(orders[i]['id']) == 'ctrl-1':
            return blocks

        blocks.append(orders[i])
    
    return blocks

def flatten_blocks(orders):
    flatten = []
    i = 0
    while i<len(orders):
        if orders[i]['id'] == 'ctrl-1':
            loop = get_blocks_in_loop(orders, i+1) 
            flatten.extend(loop * 3)
            i += len(loop) + 2
            continue

        flatten.append(orders[i])
        i += 1

    return flatten

DEFAULT_LIFETIME = 5

def get_lifetime_from_block(block):
    return DEFAULT_LIFETIME if block.get('lifetime') is None else block['lifetime']

def create_object(block):
    lifetime = get_lifetime_from_block(block)
    if block['id'] == 'object-1':
        return LedFillObject(Color(1,0,0), lifetime)
    elif block['id'] == 'object-2':
        return LedRandomRippleObject(lifetime)

def create_filter(block, canvas):
    lifetime = get_lifetime_from_block(block)
    if block['id'] == 'filter-0':
        return canvas
    elif block['id'] == 'filter-1':
        return LedHsvCanvasFilter(canvas)
    elif block['id'] == 'filter-2':
        return LedWaveCanvasFilter(canvas)

def create_block(block, canvas):
    if str(block['id']).startswith('object'):
        return create_object(block)
    elif str(block['id']).startswith('filter'):
        return create_filter(block, canvas)



