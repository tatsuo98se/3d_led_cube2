from libled.led_canvas import LedCanvas
from libled.util.led_block_util import *
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
            flatten_data = flatten_blocks(data['orders'])

            canvas = self.base_canvas
            current_block = None

            for data in flatten_data:
                if self.is_abort:
                    canvas.abort()
                    return

                current_block = create_block(data, self.base_canvas)
                if isinstance(current_block, ILedCanvas):
                    canvas = current_block
                    continue
                else:
                    canvas.add_object(current_block)

                while(True):
                    if self.is_abort:
                        canvas.abort()
                        return

                    if not isinstance(current_block, LedObject):
                        print("error unexpected type" + str(type(current_block)))
                    if isinstance(current_block, LedObject) and current_block.is_expired():
                        break

                    canvas.show()
                    led.Wait(20)

        except KeyError:
            return
        finally:
            self.is_abort = False
            self.is_running = False
            led.Clear()
            led.Show()


