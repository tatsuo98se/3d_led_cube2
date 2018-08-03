import json
from libled.led_cube import *
from datetime import datetime
import time
import traceback
from libled.led_canvas import LedCanvas
from libled.util.led_order_util import *
from libled.i_led_canvas import ILedCanvas
from libled.object.led_object import LedObject
from libled.util import sync
from libled.util.queue import Queue
from libled.object.led_fadeinout_obj_filter import LedFadeinoutOjbectFilter
from libled.util.realsense_manager import RealsenseManager
from libled.util.hw_controller_manager import HwControllerManager
from libled.util.sound_interface import SoundInterface


class LedFramework(object):

    def __init__(self, rs_host, hwctrl_host):
        self.is_running = False
        self.is_abort = False
        self.rs_host = rs_host
        self.hwctrl_host = hwctrl_host
        self.base_canvas = LedCanvas()
        self.led = LedCubeFactory.get_instance()

    def start(self):
        RealsenseManager.init(self.rs_host)
        HwControllerManager.init(self.hwctrl_host)

    def stop(self):
        RealsenseManager.stop()
        self.led.Stop()

    def get_new_canvas(self, oldcanvas):
        oldcanvas.destructer()
        return self.base_canvas


    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False

    def abort(self):
        if not self.is_running:
            return
        self.is_abort = True

    def show(self, data):
        self.is_running = True

        canvas = self.base_canvas
        current_order = None

        try:
            flatten_data = Queue(flatten_orders(data['orders']))
            overlap_time = get_overlap_time(data['orders'])
            inout_effect = True if not get_inout_effect(data['orders']) is None else False

            # save order
            logorder = datetime.now().strftime('%Y%m%d-%H-%M-%S-%f')[:-3]
            f = open('log/order_history/' + logorder + '.log', 'w')
            f.write('show:' + json.dumps(data))
            f.close()


            while(True):
                span = time.time()
                if self.is_abort:
                    canvas.abort()
                    canvas.clear()
                    break
                    
                if current_order is None:
                    data = flatten_data.dequeue()
                    if data is None:
                        if canvas.get_object_count() <= 0:
                            break
                        else:
                            pass
                    else:
                        current_order = create_order(data, canvas)

                    if isinstance(current_order, ILedCanvas):
                        canvas = current_order
                        current_order = None
                    elif isinstance(current_order, LedFilterClearCtrl):
                        SoundInterface.stop()
                        canvas = self.base_canvas
                        current_order = None
                    elif isinstance(current_order, LedObject):
                        if inout_effect:
                            current_order = LedFadeinoutOjbectFilter(current_order)

                        canvas.add_object(current_order)
                    else:
                        current_order = None

                canvas.show()
                if current_order is not None and current_order.is_expired(overlap_time):
                    current_order = None
                
                spanx = (time.time() - span) * 1000
                wait = max(0, 70 - spanx)
                #print('span: ' + str(spanx) + ' wait:' + str(wait))
                self.led.Wait(wait)

            SoundInterface.stop()
            self.led.Clear()
            self.led.Show()

        except KeyError as err:
            logger.e("error unexpected json : {0}".format(err))
            logger.e(traceback.format_exc())
            return
        finally:
            self.is_abort = False
            self.is_running = False
            canvas.clear()


