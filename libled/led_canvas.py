from led_cube import *
from i_led_canvas import ILedCanvas
from util.color import Color
from util.cube_util import *

class LedCanvas(ILedCanvas):

    def __init__(self):
        self.is_abort = False
        self.objects = []
        self.led_cube = self.get_new_canvas()

    def destructor(self):
        pass

    def get_new_canvas(self):
        return [[[Color(0,0,0,0) for _ in range(LED_DEPTH)] for _ in range(LED_HEIGHT)] for _ in range(LED_WIDTH)]

    def set_led(self, x, y, z, color):

        if color is None:
            return

        ix, iy, iz = rounds(x, y, z)
        if not is_in_cube(ix, iy, iz):
            return

        src_color = Color.object_to_color(color)

        if src_color.a == 0.0:
            return

        new_color = None
        if src_color.a != 1.0:

            dest_color = self.led_cube[ix][iy][iz]
            
            # alpha blend
            newr = dest_color.r * (1.0 - src_color.a) + src_color.r * src_color.a
            newg = dest_color.g * (1.0 - src_color.a) + src_color.g * src_color.a
            newb = dest_color.b * (1.0 - src_color.a) + src_color.b * src_color.a

            new_color = Color(newr, newg, newb)
        else:
            new_color = src_color

        if new_color.is_black():
            return
        self.led_cube[ix][iy][iz] = new_color
        led.SetLed(ix, iy, iz, int(new_color))

    def show(self, canvas=None):
        led.Clear()
        self.led_cube = self.get_new_canvas()
        for obj in self.objects[:]:
            obj.will_draw()
            #print('obj.draw()' + str(type(obj)))
            if canvas is None:
                self.pre_draw()
                obj.draw(self)
                self.post_draw()
            else:
                canvas.pre_draw()
                obj.draw(canvas)
                canvas.post_draw()
            if obj.is_expired() or obj.is_cancel():
                self.remove_object(obj)

        led.Show()

    def pre_draw(self):
        pass
    
    def post_draw(self):
        pass

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        obj.did_detach()

    def clear_object(self):
        self.objects = []

    def abort(self):
        self.is_abort = True
        for obj in self.objects[:]:
            obj.abort()

    def clear(self):
        for obj in self.objects[:]:
            obj.abort()
        self.objects = []

    def get_object_count(self):
        return len(self.objects)
