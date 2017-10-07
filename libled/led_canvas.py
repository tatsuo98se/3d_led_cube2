from led_cube import *
from i_led_canvas import ILedCanvas
from util.color import Color

class LedCanvas(ILedCanvas):

    def __init__(self):
        self.is_abort = False
        self.objects = []
        self.led_cube = self.get_new_canvas()

    def get_new_canvas(self):
        return [[[Color(0,0,0,0) for depth in range(LED_DEPTH)] for height in range(LED_HEIGHT)] for width in range(LED_WIDTH)]

    def set_led(self, x, y, z, color):
        ix = int(round(x))
        iy = int(round(y))
        iz = int(round(z))

        if ix < 0 or ix >= LED_WIDTH:
            return

        if iy < 0 or iy >= LED_HEIGHT:
            return

        if iz < 0 or iz >= LED_DEPTH:
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
                obj.draw(self)
            else:
                obj.draw(canvas)
            if obj.is_expired() or obj.is_cancel():
                self.objects.remove(obj)

        led.Show()

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

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
        led.Clear()
        led.Show()
