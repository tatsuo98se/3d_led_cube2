from color import Color
import base64
import cStringIO
from ..led_canvas import LedCanvas
from ..object.led_overlapped_object import LedOverlappedObject
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
from ..object.led_fireworks_obj import LedFireworksObject
from ..object.led_balls_obj import LedBallsObject
from ..object.led_mario_jump_obj import LedMarioJumpObject
from ..object.led_mario_runjump_obj import LedMarioRunJumpObject
from ..object.led_drop_mushroom_obj import LedDropMushroomObject
from ..object.led_scrolled_bitmap_obj import LedScrolledBitmapObject
from ..object.led_mario_get_mushroom_obj import LedMarioGetMushroomObject

from ..led_canvas import LedCanvas
from ..filter.led_canvs_filter import LedCanvasFilter
from ..filter.led_test_canvas_filter import LedTestCanvasFilter
from ..filter.led_wave_canvas_filter import LedWaveCanvasFilter
from ..filter.led_flat_wave_canvas_filter import LedFlatWaveCanvasFilter
from ..filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from ..filter.led_skewed_canvas_filter import LedSkewedCanvasFilter


def get_orders_in_loop(orders, start):
    orders_in_loop = []
    for i in range(start, len(orders)):
        if str(orders[i]['id']) == 'ctrl-loop':
            return orders_in_loop

        orders_in_loop.append(orders[i])
    
    return orders_in_loop

def get_param(order, key, default = None):
    param = order.get(key)
    return default if param is None else param

def flatten_orders(orders):
    flatten = []
    i = 0
    while i<len(orders):
        if orders[i]['id'] == 'ctrl-loop':
            count = get_param(orders[i], 'count', 3)
            loop = get_orders_in_loop(orders, i+1) 
            flatten.extend(loop * count)
            i += len(loop) + 2
            continue

        flatten.append(orders[i])
        i += 1

    return flatten

DEFAULT_LIFETIME = 5

def create_object(order):
    oid = order['id']
    lifetime = get_param(order, 'lifetime', DEFAULT_LIFETIME)
    z = get_param(order, 'z', 0)
    y = get_param(order, 'y', 0)
    cycle = get_param(order, 'cycle')
    overlap = get_param(order, 'overlap', False)
    obj = None

    if oid == 'object-clear':
        obj = LedClearObject(lifetime)
    if oid== 'object-fill':
        obj = LedFillObject(Color(1,0,0), lifetime)
    elif oid == 'object-ripple':
        obj = LedRandomRippleObject(lifetime)
    elif oid == 'object-mario':
        obj = LedBitmapObject('asset/image/mario.png', 0, 0, z, lifetime)
    elif oid == 'object-mario-run1':
        obj = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, z, lifetime)
    elif oid == 'object-mario-run2':
        obj = LedBitmapObject('asset/image/mario_run_2.png', 0, 0, z, lifetime)
    elif oid == 'object-s-mario':
        obj = LedBitmapObject('asset/image/s_mario.png', 0, 0, z, lifetime)
    elif oid == 'object-s-mario-run1':
        obj = LedBitmapObject('asset/image/s_mario_run_1.png', 0, 0, z, lifetime)
    elif oid == 'object-s-mario-run2':
        obj = LedBitmapObject('asset/image/s_mario_run_2.png', 0, 0, z, lifetime)
    elif oid == 'object-mario-run-anime':
        obj = LedMarioRunObject(z, lifetime)
    elif oid == 'object-bitmap':
        image = get_param(order, 'bitmap')
        if image is None:
            raise KeyError('id:{0} bitmap key was not specified.'.format(oid))
        try:
            obj = LedBitmapObject(cStringIO.StringIO(base64.b64decode(image)), 0, 0, z, lifetime)

        except:
            raise KeyError('id:{0} image decode error.'.format(oid))

    elif oid == 'object-cube':
        obj = LedCubeObject(lifetime)
    elif oid == 'object-sphere':
        obj = LedSphereObject(lifetime)
    elif oid == 'object-repbang':
        obj = LedRepbangObject(lifetime)
    elif oid == 'object-skewed-sphere':
        obj = LedSkewedSphereObject(lifetime)
    elif oid == 'object-skewed-cube':
        obj = LedSkewedCubeObject(lifetime)
    elif oid == 'object-fireworks':
        obj = LedFireworksObject(lifetime)
    elif oid == 'object-balls':
        obj = LedBallsObject(lifetime)
    elif oid == 'object-mario-jump-anime':
        obj = LedMarioJumpObject(y, z, lifetime)
    elif oid == 'object-mario-runandjump-anime':
        obj = LedMarioRunJumpObject(y, z, lifetime)
    elif oid == 'object-mario-get-mushroom':
        obj = LedMarioGetMushroomObject(z)
    elif oid == 'object-drop-mushroom':
        obj = LedDropMushroomObject(z, lifetime)
    elif oid == 'object-bk-mountain':
        obj = LedScrolledBitmapObject('asset/image/background_mountain.png', 0, y, z, cycle, lifetime)
    elif oid == 'object-bk-grass':
        obj = LedScrolledBitmapObject('asset/image/background_grass.png', 0, y, z, cycle, lifetime)
    elif oid == 'object-bk-cloud':
        obj = LedScrolledBitmapObject('asset/image/background_cloud.png', 0, y, z, cycle, lifetime)
    else:
        raise KeyError('unknown object id:{0}'.format(oid))

    if overlap:
        return LedOverlappedObject(obj)
    else:
        return obj


def create_filter(order, canvas):
    oid = order['id']
    if oid == 'filter-clear':
        return canvas
    elif oid == 'filter-hsv':
        return LedHsvCanvasFilter(canvas)
    elif oid == 'filter-wave':
        return LedWaveCanvasFilter(canvas)
    elif oid == 'filter-flat-wave':
        return LedFlatWaveCanvasFilter(canvas)
    elif oid == 'filter-skewed':
        return LedSkewedCanvasFilter(canvas)
    else:
        raise KeyError('unknown filter id:{0} i'.format(oid))

def create_order(order, canvas):
    oid = order['id']
    if oid.startswith('object'):
        return create_object(order)
    elif oid.startswith('filter'):
        return create_filter(order, canvas)
    elif oid.startswith('ctrl'):
        return None
    else:
        raise KeyError('unknown id prefix:{0} i'.format(oid))

def get_ctrl(orders, ctrl_id):
    for order in orders:
        if order['id'].startswith(ctrl_id):
            return order

    return None

def get_overlap_time(orders):
    ctrl = get_ctrl(orders, 'ctrl-overlap')
    if ctrl is None:
        return 0
    return get_param(ctrl, 'time', 2)

def get_inout_effect(orders):
    ctrl = get_ctrl(orders, 'ctrl-inout-effect')
    if ctrl is None:
        return None
    return 1
