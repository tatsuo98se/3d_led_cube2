import time

class TimerUtil:
    def __init__(self):
        self.born_at = 0
        self.callback = None
        self.last_update = 0.0
        self.timer = None

    def elapsed(self):
        return time.time() - self.born_at

    def set_timer(self, timer, callback):
        self.timer = timer
        self.callback = callback

    def is_timer_set(self):
        return self.callback is not None

    def reset_timer(self):
        self.timer = None
        self.callback = None

    def start(self):
        if self.born_at == 0:
            self.born_at = time.time()

    def update_timer(self):
        self.start()

        if self.timer == 0:
            self.callback.on_timer()
            return

        if self.timer is not None:
            if self.last_update == 0:
                self.last_update = self.elapsed()
                
            if self.elapsed() - self.last_update > self.timer:
                self.last_update = self.elapsed()
                self.callback.on_timer()
        