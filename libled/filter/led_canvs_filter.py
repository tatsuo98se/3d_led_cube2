from ..i_led_canvas import ILedCanvas
from ..util.hw_controller_manager import HwControllerManager as hcm
from ..util.timer_util import TimerUtil
from ..util.logger import *

class LedCanvasFilter(ILedCanvas):

    def __init__(self, canvas, enable_controller=False):
        self.canvas = canvas
        self.enable_controller = enable_controller
        self.timer = TimerUtil()

    def destructer(self):
        self.canvas.destructor()

    def set_led(self, x, y, z, color):
        self.canvas.set_led(x, y, z, color)

    def show(self, canvas=None):
        if canvas is None:
            self.canvas.show(self)
        else:
            self.canvas.show(canvas)

    def pre_draw(self):
        self.timer.update_timer()
        self.canvas.pre_draw()
    
    def post_draw(self):
        self.canvas.post_draw()

    def add_object(self, obj):
        self.canvas.add_object(obj)

    def remove_object(self, obj):
        self.canvas.remove_object(obj)
        
    def clear_object(self):
        self.canvas.clear_object()

    def abort(self):
        self.canvas.abort()

    def clear(self):
        self.canvas.clear()
    
    def get_object_count(self):
        self.canvas.get_object_count()

    def has(self, target_filters):
        
        canvas = self
        
        while True:
            if not isinstance(canvas, LedCanvasFilter):
                return False

            if isinstance(target_filters, list):
                for filter in target_filters:
                    if type(canvas) == filter:
                        return True
            else:
                if type(canvas) == target_filters:
                    return True

            canvas = canvas.canvas

    def get_param_from_controller(self, defaults = None):
        if not self.enable_controller:
            return defaults

        data =  hcm.get_data()
        if data is not None and data != '':
            return data
        else:
            return defaults
        
    def set_timer(self, timer, callback):
        self.timer.set_timer(timer, callback)

    def reset_timer(self):
        self.timer.reset_timer()

    def on_timer(self):
        e('you should implement on_timer on your filter class.')
        
            
