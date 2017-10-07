import json
from datetime import datetime
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

    def abort(self):
        if not self.is_running:
            return
        self.is_abort = True

    def show(self, dic):
        self.is_running = True
        led = dic['led']
        data = dic['orders']

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
                if self.is_abort:
                    canvas.abort()
                    return

                if current_order is None:
                    data = flatten_data.dequeue()
                    if data is None:
                        return
                    current_order = create_order(data, self.base_canvas)

                    if isinstance(current_order, ILedCanvas):
                        canvas = current_order
                        current_order = None
                        continue
                    elif isinstance(current_order, LedObject):
                        if inout_effect:
                            current_order = LedFadeinoutOjbectFilter(current_order)

                        canvas.add_object(current_order)

                    else:
                        current_order = None
                        continue

                if current_order.is_expired(overlap_time):
                    current_order = None

                canvas.show()
                led.Wait(20)

        except KeyError:
            print("error unexpected json")
            return
        finally:
            self.is_abort = False
            self.is_running = False
            canvas.clear()


