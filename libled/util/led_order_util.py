from color import Color
import base64
import cStringIO
from ..led_canvas import LedCanvas
from ..object.led_dot_obj import LedDotObject
from ..object.led_ripple_obj import LedRippleObject
from ..object.led_fill_obj import LedFillObject
from ..object.led_random_ripple_obj import LedRandomRippleObject
from ..object.led_clear_obj import LedClearObject
from ..object.led_bitmap_obj import LedBitmapObject
from ..object.led_mario_run_obj import LedMarioRunObject
from ..object.led_cube_obj import LedCubeObject
from ..object.led_sphere_obj import LedSphereObject
from ..object.led_repbang_obj import LedRepbangObject
from ..object.led_skewed_sphere_obj import LedSkewedSphereObject
from ..object.led_skewed_cube_obj import LedSkewedCubeObject

from ..led_canvas import LedCanvas
from ..filter.led_canvs_filter import LedCanvasFilter
from ..filter.led_test_canvas_filter import LedTestCanvasFilter
from ..filter.led_wave_canvas_filter import LedWaveCanvasFilter
from ..filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from ..filter.led_skewed_canvas_filter import LedSkewedCanvasFilter

from PIL import Image


def get_orders_in_loop(orders, start):
    orders_in_loop = []
    for i in range(start, len(orders)):
        if str(orders[i]['id']) == 'ctrl-loop':
            return orders_in_loop

        orders_in_loop.append(orders[i])
    
    return orders_in_loop

def get_lifetime_from_order(order):
    return DEFAULT_LIFETIME if order.get('lifetime') is None else order['lifetime']

def get_param_from_order(order, key):
    param = order.get('param')
    if param is None:
        return None

    return param.get(key)

def flatten_orders(orders):
    flatten = []
    i = 0
    while i<len(orders):
        if orders[i]['id'] == 'ctrl-loop':
            count = get_param_from_order(orders[i], 'count')
            count = 3 if count is None else count
            loop = get_orders_in_loop(orders, i+1) 
            flatten.extend(loop * count)
            i += len(loop) + 2
            continue

        flatten.append(orders[i])
        i += 1

    return flatten

DEFAULT_LIFETIME = 5


def create_object(order):
    lifetime = get_lifetime_from_order(order)
    oid = order['id']
    z = get_param_from_order(order, 'z')
    z = 0 if z is None else z
    if oid == 'object-clear':
        return LedClearObject(lifetime)
    if oid== 'object-fill':
        return LedFillObject(Color(1,0,0), lifetime)
    elif oid == 'object-ripple':
        return LedRandomRippleObject(lifetime)
    elif oid == 'object-mario':
        return LedBitmapObject(Image.open('contents/s_mario.png'), z, lifetime)
    elif oid == 'object-mario-run1':
        return LedBitmapObject(Image.open('contents/s_mario_run_1.png'), z, lifetime)
    elif oid == 'object-mario-run2':
        return LedBitmapObject(Image.open('contents/s_mario_run_2.png'), z, lifetime)
    elif oid == 'object-mario-run-anime':
        return LedMarioRunObject(z, lifetime)
    elif oid == 'object-bitmap':
        image = get_param_from_order(order, 'bitmap')
        if image is None:
            raise KeyError
        try:
            return LedBitmapObject(Image.open(cStringIO.StringIO(base64.b64decode(image))), z, lifetime)

        except:
            print("image decode error")
            raise KeyError
    elif oid == 'object-cube':
        return LedCubeObject(lifetime)
    elif oid == 'object-sphere':
        return LedSphereObject(lifetime)
    elif oid == 'object-repbang':
        return LedRepbangObject(lifetime)
    elif oid == 'object-skewed-sphere':
        return LedSkewedSphereObject(lifetime)
    elif oid == 'object-skewed-cube':
        return LedSkewedCubeObject(lifetime)
    else:
        raise KeyError

def create_filter(order, canvas):
    oid = order['id']
    if oid == 'filter-clear':
        return canvas
    elif oid == 'filter-hsv':
        return LedHsvCanvasFilter(canvas)
    elif oid == 'filter-wave':
        return LedWaveCanvasFilter(canvas)
    elif oid == 'filter-skewed':
        return LedSkewedCanvasFilter(canvas)
    else:
        raise KeyError

def create_order(order, canvas):
    oid = order['id']
    if oid.startswith('object'):
        return create_object(order)
    elif oid.startswith('filter'):
        return create_filter(order, canvas)
    else:
        raise KeyError



