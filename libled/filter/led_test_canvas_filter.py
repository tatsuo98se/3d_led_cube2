from led_canvs_filter import LedCanvasFilter

class LedTestCanvasFilter(LedCanvasFilter):

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, 0xff0000)

