from led_object import LedObject
from ..object.led_mario_run_obj import LedMarioRunObject
from ..object.led_mario_jump_obj import LedMarioJumpObject

SEC = 100 / 20
RUN_TIME = 5 * SEC
JUMP_TIME = 6 * SEC

class LedMarioRunJumpObject(LedObject):

    def __init__(self, y, z, lifetime=0):
        super(LedMarioRunJumpObject, self).__init__(lifetime)
        self.run = LedMarioRunObject(z)
        self.jump = LedMarioJumpObject(y, z)
        self.running = True
        self.time = 0

    def draw(self, canvas):
        if self.running and self.time >= RUN_TIME:
            self.running = False
            self.time = 0
        elif (not self.running) and self.time >= JUMP_TIME:
            self.running = True
            self.time = 0

        if self.running:
            self.run.draw(canvas)
        else:
            self.jump.draw(canvas)

        self.time += 1

    def will_draw(self):
        self.run.will_draw()

    def set_timer(self, timer):
        self.run.set_timer()

    def rest_timer(self):
        self.run.rest_timer()

    def on_timer(self):
        self.run.on_timer()

    def abort(self):
        self.run.abort()
