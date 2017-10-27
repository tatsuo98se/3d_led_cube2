from led_canvs_filter import LedCanvasFilter

class _DummyFilter(LedCanvasFilter):

    def __init__(self, canvas):
        super(_DummyFilter, self).__init__(canvas)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        obj.did_detach()

    def clear_object(self):
        self.objects = []

    def get_object_count(self):
        return len(self.objects)

    def get_objects(self):
        return self.objects

class LedObjectCanvasFilter(LedCanvasFilter):

    def __init__(self, canvas, obj):
        super(LedObjectCanvasFilter, self).__init__(canvas)
        self._dummy_filter = _DummyFilter(canvas)
        self._dummy_filter.add_object(obj)
    
    def pre_draw(self):
        super(LedObjectCanvasFilter, self).pre_draw()

        objects = self._dummy_filter.get_objects()
        for obj in objects:
            obj.will_draw()
            obj.draw(self._dummy_filter)

            if obj.is_expired():
                 self._dummy_filter.remove_object(obj)

