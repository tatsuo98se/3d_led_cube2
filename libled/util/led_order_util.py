# coding:utf-8
from color import Color
import base64
import cStringIO
import block_dictionary
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
from ..object.led_text_obj import LedTextObject
from ..object.led_heart_obj import LedHeartObject
from ..object.led_snows_obj import LedSnowsObject
from ..object.led_star_obj import LedStarObject
from ..object.led_wave_obj import LedWaveObject
from ..object.led_tree_obj import LedTreeObject
from ..object.led_twinkle_stars_obj import LedTwinkleStartsObject
from ..object.led_snowman_obj import LedSnowmanObject
from ..object.led_ghost_obj import LedGhostObject
from ..object.led_note_obj import LedNoteObject
from ..object.led_elefant_obj import LedElefantObject
from ..object.led_socks_obj import LedSocksObject
from ..object.led_stickman_obj import LedStickmanObject
from ..object.led_yacht_obj import LedYachtObject
from ..object.led_leafs_obj import LedLeafsObject
from ..object.led_clouds_obj import LedCloudsObject
from ..object.led_scrolled_mountain_obj import LedScrolledMountainObject
from ..object.led_scrolled_grass_obj import LedScrolledGrassObject
from ..object.led_realsense_obj import LedRealsenseObject
from ..object.led_makey_obj import LedMakeyObject
from ..object.led_painting_obj import LedPaintingObject
from ..object.led_3d_makey_obj import Led3DMakeyObject

from ..led_canvas import LedCanvas
from ..filter.led_canvs_filter import LedCanvasFilter
from ..filter.led_test_canvas_filter import LedTestCanvasFilter
from ..filter.led_wave_canvas_filter import LedWaveCanvasFilter
from ..filter.led_flat_wave_canvas_filter import LedFlatWaveCanvasFilter
from ..filter.led_hsv_canvas_filter import LedHsvCanvasFilter
from ..filter.led_jump_canvas_filter import LedJumpCanvasFilter
from ..filter.led_rainbow_canvas_filter import LedRainbowCanvasFilter
from ..filter.led_object_canvas_filter import LedObjectCanvasFilter
from ..filter.led_bk_snows_object_canvas_filter import LedSnowsObjectCanvasFilter
from ..filter.led_zoom_in_out_canvas_filter import LedZoomInOutCanvasFilter
from ..filter.led_spiral_canvas_filter import LedSpiralCanvasFilter
from ..filter.led_spiral_canvas_filter2 import LedSpiralCanvasFilter2
from ..filter.led_swaying_canvas_filter import LedSwayingCanvasFilter
from ..filter.led_bk_wave_object_canvas_filter import LedWaveObjectCanvasFilter
from ..filter.led_bk_sakura_object_canvas_filter import LedSakuraObjectCanvasFilter
from ..filter.led_color_ctrl_canvas_filter import LedColorCtrlCanvasFilter
from ..filter.led_wakame_canvas_filter import LedWakameCanvasFilter
from ..filter.led_vibe_canvas_filter import LedVibeCanvasFilter
from ..filter.led_rolling_canvas_filter import LedRollingCanvasFilter
from ..filter.led_skewed_canvas_filter import LedSkewedCanvasFilter
from ..filter.led_jump_button_canvas_filter import LedJumpButtonCanvasFilter
from ..filter.led_exile_canvas_filter import LedExileCanvasFilter
from ..filter.led_zanzo_canvas_filter import LedZanzoCanvasFilter
from ..filter.led_3d_zanzo_canvas_filter import Led3DZanzoCanvasFilter
from ..filter.led_explosion_canvas_filter import LedExplosionCanvasFilter

from ..ctrl.led_filter_clear_ctrl import LedFilterClearCtrl

def get_orders_in_loop(orders, start):
    orders_in_loop = []
    for i in range(start, len(orders)):
        if 'id' in orders[i] and str(orders[i]['id']) == 'ctrl-loop':
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
        if 'id' in orders[i] and orders[i]['id'] == 'ctrl-loop':
            count = get_param(orders[i], 'count', 3)
            loop = get_orders_in_loop(orders, i+1) 
            flatten.extend(loop * count)
            i += len(loop) + 2
            continue

        flatten.append(orders[i])
        i += 1

    return flatten

DEFAULT_LIFETIME = 13 # 2017.11.13 検証結果 コレぐらいの時間がちょうどいい

def create_object(order):
    oid = order['id']
    lifetime = get_param(order, 'lifetime', DEFAULT_LIFETIME)
    z = get_param(order, 'z', 0)
    y = get_param(order, 'y', 0)
    x = get_param(order, 'x', 0)
    thick = get_param(order, 'thick', 1)
    cycle = get_param(order, 'cycle')
    overlap = get_param(order, 'overlap', False)
    obj = None

    if oid == 'object-clear':
        obj = LedClearObject(lifetime)
    if oid== 'object-fill-white':
        obj = LedFillObject(Color(0.5,0.5,0.5), lifetime)
    elif oid == 'object-ripple':
        obj = LedRandomRippleObject(lifetime)
    elif oid == 'object-mario':
        obj = LedBitmapObject('asset/image/mario.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-mario-run1':
        obj = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-mario-run2':
        obj = LedBitmapObject('asset/image/mario_run_2.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-mario-jump':
        obj = LedBitmapObject('asset/image/mario_jump.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-s-mario':
        obj = LedBitmapObject('asset/image/s_mario.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-s-mario-run1':
        obj = LedBitmapObject('asset/image/s_mario_run_1.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-s-mario-run2':
        obj = LedBitmapObject('asset/image/s_mario_run_2.png', 0, 0, z, thick, lifetime)
    elif oid == 'object-snow-crystal':
        obj = LedBitmapObject('asset/image/snow_crystal_1.png', 0, 0, 4, 2, lifetime)
    elif oid == 'object-star':
        obj = LedStarObject(x, y, z, lifetime)
    elif oid == 'object-heart':
        obj = LedHeartObject(x, y, z, lifetime)
    elif oid == 'object-tree':
        mode = get_param(order, 'mode', None)
        obj = LedTreeObject(x, y, z, mode, lifetime)
    elif oid == 'object-snowman':
        obj = LedSnowmanObject(x, y, z, lifetime)
    elif oid == 'object-ghost':
        mode = get_param(order, 'mode', None)
        obj = LedGhostObject(x, y, z, mode, lifetime)
    elif oid == 'object-note':
        obj = LedNoteObject(x, y, z, lifetime)
    elif oid == 'object-elefant':
        obj = LedElefantObject(x, y, z, lifetime)
    elif oid == 'object-socks':
        obj = LedSocksObject(lifetime)
    elif oid == 'object-stickman':
        obj = LedStickmanObject(x, y, z, lifetime)
    elif oid == 'object-yacht':
        obj = LedYachtObject(x, y, z, lifetime)
    elif oid == 'object-mario-run-anime':
        obj = LedMarioRunObject(z, lifetime)
    elif oid == 'object-bitmap':
        image = get_param(order, 'bitmap')
        if image is None:
            raise KeyError('id:{0} bitmap key was not specified.'.format(oid))
        try:
            obj = LedBitmapObject(cStringIO.StringIO(base64.b64decode(image)), 0, 0, z, thick, lifetime)

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
    elif oid == 'object-realsense':
        obj = LedRealsenseObject(lifetime)
    elif oid == 'object-makey':
        makeytype = get_param(order, 'type')
        obj = LedMakeyObject(x, y, z, lifetime, makeytype)
    elif oid == 'object-3d-makey':
        obj = Led3DMakeyObject(x, y, z, lifetime)
    elif oid == 'object-painting':
        obj = LedPaintingObject(lifetime)
    elif oid == 'object-text':
        x = get_param(order, 'x', 15) # LED_WIDTH -1
        size = get_param(order, 'size', 26)
        color = get_param(order, 'color', '#ff0000')
        string = get_param(order, 'text', u'日本語サンプル')
        obj = LedTextObject(x=x, y=y, z=z, text=string, fontsize=size, color=color, lifetime=lifetime)
    else:
        raise KeyError('unknown object id:{0}'.format(oid))

    if overlap:
        return LedOverlappedObject(obj)
    else:
        return obj


def create_filter(order, canvas):
    oid = order['id']
    y = get_param(order, 'y', 0)
    x = get_param(order, 'x', 0)
    thick = get_param(order, 'thick', 1)
    cycle = get_param(order, 'cycle')

    if oid == 'filter-hsv':
        return LedHsvCanvasFilter(canvas)
    elif oid == 'filter-wave':
        return LedWaveCanvasFilter(canvas)
    elif oid == 'filter-flat-wave':
        return LedFlatWaveCanvasFilter(canvas)
    elif oid == 'filter-skewed':
        return LedSkewedCanvasFilter(canvas)
    elif oid == 'filter-skewed-ctrl':
        return LedSkewedCanvasFilter(canvas, enable_controller=True)
    elif oid == 'filter-z-skewed-ctrl':
        return LedSkewedCanvasFilter(canvas, ['z'], enable_controller=True)
    elif oid == 'filter-zy-skewed-ctrl':
        return LedSkewedCanvasFilter(canvas, ['z', 'y'], enable_controller=True)
    elif oid == 'filter-jump':
        return LedJumpCanvasFilter(canvas)
    elif oid == 'filter-rainbow':
        return LedRainbowCanvasFilter(canvas)
    elif oid == 'filter-zoom':
        return LedZoomInOutCanvasFilter(canvas)
    elif oid == 'filter-zoom-ctrl':
        return LedZoomInOutCanvasFilter(canvas, True)
    elif oid == 'filter-spiral':
        return LedSpiralCanvasFilter(canvas)
    elif oid == 'filter-spiral2':
        return LedSpiralCanvasFilter2(canvas)
    elif oid == 'filter-swaying':
        return LedSwayingCanvasFilter(canvas)
    elif oid == 'filter-color-ctrl':
        return LedColorCtrlCanvasFilter(canvas)
    elif oid == 'filter-rainbow-ctrl':
        return LedRainbowCanvasFilter(canvas, True)
    elif oid == 'filter-jump-ctrl':
        return LedJumpCanvasFilter(canvas, True)
    elif oid == 'filter-jump-button':
        return LedJumpButtonCanvasFilter(canvas)
    elif oid == 'filter-rolling-ctrl':
        return LedRollingCanvasFilter(canvas, True, True)
    elif oid == 'filter-rolldown':
        return LedRollingCanvasFilter(canvas)
    elif oid == 'filter-rollup':
        return LedRollingCanvasFilter(canvas, False)
    elif oid == 'filter-wakame':
        return LedWakameCanvasFilter(canvas)
    elif oid == 'filter-wakame-ctrl':
        return LedWakameCanvasFilter(canvas, True)
    elif oid == 'filter-vibe':
        return LedVibeCanvasFilter(canvas)
    elif oid == 'filter-exile':
        return LedExileCanvasFilter(canvas)
    elif oid == 'filter-zanzo':
        return LedZanzoCanvasFilter(canvas)
    elif oid == 'filter-zanzo-ctrl':
        return LedZanzoCanvasFilter(canvas, True)
    elif oid == 'filter-3d-zanzo':
        return Led3DZanzoCanvasFilter(canvas)
    elif oid == 'filter-explosion':
        return LedExplosionCanvasFilter(canvas, 2)
    elif oid == 'filter-3d-explosion':
        return LedExplosionCanvasFilter(canvas)
    elif oid == 'filter-explosion-ctrl':
        return LedExplosionCanvasFilter(canvas, 2, True)
    elif oid == 'filter-3d-explosion-ctrl':
        return LedExplosionCanvasFilter(canvas, True)
    elif oid == 'filter-bk-mountain':
        return LedObjectCanvasFilter(canvas, \
                LedScrolledMountainObject())
    elif oid == 'filter-bk-grass':
        return LedObjectCanvasFilter(canvas, \
                LedScrolledGrassObject())
    elif oid == 'filter-bk-cloud':
        return LedObjectCanvasFilter(canvas, LedCloudsObject())
    elif oid == 'filter-bk-sakura':
        return LedSakuraObjectCanvasFilter(canvas)
    elif oid == 'filter-bk-wave':
        return LedWaveObjectCanvasFilter(canvas)
    elif oid == 'filter-bk-snows':
        return LedSnowsObjectCanvasFilter(canvas)
    elif oid == 'filter-bk-stars':
        return LedObjectCanvasFilter(canvas, \
                LedTwinkleStartsObject())
    elif oid == 'filter-bk-fireworks':
        return LedObjectCanvasFilter(canvas, \
                LedFireworksObject())
    else:
        raise KeyError('unknown filter id:{0} i'.format(oid))

def create_ctrl(order):
    oid = order['id']
    if oid == 'ctrl-filter-clear':
        return LedFilterClearCtrl()
    else:
        return None

def create_order(order, canvas):
    if 'id' not in order:
        order['id'] = block_dictionary.convert_json(order)

    oid = order['id']
    if oid.startswith('object'):
        return create_object(order)
    elif oid.startswith('filter'):
        return create_filter(order, canvas)
    elif oid.startswith('ctrl'):
        return create_ctrl(order)
    else:
        raise KeyError('unknown id prefix:{0} i'.format(oid))

def get_ctrl(orders, ctrl_id):
    for order in orders:
        if 'id' in order and order['id'].startswith(ctrl_id):
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
