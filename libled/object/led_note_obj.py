from led_bitmaps_obj import LedBitmapsObject

class LedNoteObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime = 0 ):
        super(LedNoteObject, self).__init__( \
            [
                'asset/image/note/eighth1.png',
                'asset/image/note/eighth2.png',
                'asset/image/note/eighth3.png',
                'asset/image/note/eighth4.png',
                'asset/image/note/eighth4.png',
                'asset/image/note/eighth3.png',
                'asset/image/note/eighth2.png',
                'asset/image/note/eighth1.png',
            ],
            x, y, z, 
            lifetime)
