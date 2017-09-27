from libled.led_canvas import LedCanvas
from libled.util.led_order_util import *
from libled.i_led_canvas import ILedCanvas
from libled.object.led_object import LedObject
from libled.util import sync

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

        try:
            flatten_data = flatten_orders(data['orders'])

            canvas = self.base_canvas
            current_order = None

            for data in flatten_data:
                if self.is_abort:
                    canvas.abort()
                    return

                current_order = create_order(data, self.base_canvas)
                if isinstance(current_order, ILedCanvas):
                    canvas = current_order
                    continue
                else:
                    canvas.add_object(current_order)

                while(True):
                    if self.is_abort:
                        canvas.abort()
                        return

                    if not isinstance(current_order, LedObject):
                        print("error unexpected type" + str(type(current_order)))
                    if isinstance(current_order, LedObject) and current_order.is_expired():
                        break

                    canvas.show()
                    led.Wait(20)

        except KeyError:
            print("error unexpected json")
            return
        finally:
            self.is_abort = False
            self.is_running = False
            canvas.clear()


