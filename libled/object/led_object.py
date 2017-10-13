import time
from ..util import sync
from abc import ABCMeta, abstractmethod

class LedObject(object):

    myLock = sync.create_lock()

    def __init__(self, lifetime=0):
        self.born_at = 0
        self.lifetime = lifetime
        self.is_abort = False
        self.last_update = 0.0
        self.timer = 0

    def elapsed(self):
        return time.time() - self.born_at

    def is_expired(self, offset = 0):
        if self.lifetime == 0 or self.born_at == 0:
            return False

        if self.lifetime - offset < time.time() - self.born_at:
            return True

        return False

    @abstractmethod
    def draw(self, canvas):
        pass

    @sync.synchronized(myLock)
    def abort(self):
        self.is_abort = True

    @sync.synchronized(myLock)
    def is_cancel(self):
        return self.is_abort

    def will_draw(self):
        if self.born_at == 0:
            self.born_at = time.time()
        if self.timer != 0:
            if self.last_update == 0:
                self.last_update = self.elapsed()
                
            if self.elapsed() - self.last_update > self.timer:
                self.last_update = self.elapsed()
                self.on_timer()

    def set_timer(self, timer):
        self.timer = timer

    def reset_timer(self):
        self.timer = 0

    def on_timer(self):
        pass