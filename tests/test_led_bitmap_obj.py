import unittest
from libled.object.led_bitmap_obj import LedBitmapObject

class TestLedBitmapObject(unittest.TestCase):

    def test_1(self):
        mario0 = LedBitmapObject('asset/image/mario.png', 0, 0, 0, 10)
        mario1 = LedBitmapObject('asset/image/mario_run_1.png', 0, 0, 0, 10)
        mario2 = LedBitmapObject('asset/image/mario_run_2.png', 0, 0, 0, 10)

        self.assertIsNotNone(mario0)
        self.assertIsNotNone(mario1)
        self.assertIsNotNone(mario2)
