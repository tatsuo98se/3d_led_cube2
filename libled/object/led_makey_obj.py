from led_bitmaps_obj import LedBitmapsObject
from ..led_cube import *

class LedMakeyObject(LedBitmapsObject):

    def __init__(self, x=0, y=0, z=0, lifetime=0, makeytype='one'):
        super(LedMakeyObject, self).__init__(None, x, y, z, lifetime)

        makey_one = \
            [
                'asset/image/makey/makey1.png',
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        makey_two = \
            [
                'asset/image/makey/makey2.png',
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        makey_three = \
            [
                'asset/image/makey/makey3.png',
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        makey_dic = {'one': makey_one, 
                  'two': makey_two, 
                  'three': makey_three}

        print('type = {}'.format(makeytype))
        if makeytype in makey_dic:
            makey = makey_dic[makeytype]
        else:
            makey = makey_one

        self.init_images(makey)
