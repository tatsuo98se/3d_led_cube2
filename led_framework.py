from libled.led_canvas import LedCanvas
from libled.util.led_block_util import *
from libled.i_led_canvas import ILedCanvas
from libled.object.led_object import LedObject

def show(led, data):

    flatten_data = flatten_blocks(data)

    base_canvas = LedCanvas()
    canvas = base_canvas
    current_block = None

    for data in flatten_data:
        current_block = create_block(data, base_canvas)
        if isinstance(current_block, ILedCanvas):
            canvas = current_block
            continue
        else:
            canvas.add_object(current_block)

        while(True):
            assert isinstance(current_block, LedObject)
            if isinstance(current_block, LedObject) and current_block.is_expired():
                break

            canvas.show()
            led.Wait(20)

