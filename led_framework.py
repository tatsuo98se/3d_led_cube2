import json
from libled.led_cube import *
from datetime import datetime
import time
from libled.util.serial_manager import SerialManager
from libled.util.realsense_manager import RealsenseManager
from libled.led_canvas import LedCanvas
from libled.util.led_order_util import *
from libled.i_led_canvas import ILedCanvas
from libled.object.led_object import LedObject
from libled.util import sync
from libled.util.queue import Queue
from libled.object.led_fadeinout_obj_filter import LedFadeinoutOjbectFilter

class LedFramework(object):

    def __init__(self):
        self.is_running = False
        self.is_abort = False
        self.base_canvas = LedCanvas()
        SerialManager.init()
        RealsenseManager.init()

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
                    return

                if current_order is None:
                    data = flatten_data.dequeue()
                    if data is None:
                        if canvas.get_object_count() <= 0:
                            return
                        else:
                            pass
                    else:
                        current_order = create_order(data, canvas)

                    if isinstance(current_order, ILedCanvas):
                        canvas = current_order
                        current_order = None
                    elif isinstance(current_order, LedFilterClearCtrl):
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
                led.Wait(wait)

        except KeyError as err:
            print("error unexpected json : {0}".format(err))
            return
        finally:
            self.is_abort = False
            self.is_running = False
            SerialManager.stop()
            canvas.clear()
            led.Show()


