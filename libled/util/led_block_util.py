from ..object.led_dot_obj import LedDotObject
from ..led_canvas import LedCanvas
from ..filter.led_test_canvas_filter import LedTestCanvasFilter

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

def create_object(block):
    return None

def create_filter(block):
    return None

def create_block(block):
    if str(block).startswith('object'):
        return create_object(block)
    elif str(block).startswith('filter'):
        return create_filter(block)



