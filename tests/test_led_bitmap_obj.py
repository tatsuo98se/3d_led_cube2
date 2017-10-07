import unittest
from libled.object.led_bitmap_obj import LedBitmapObject
from PIL import Image

class TestLedBitmapObject(unittest.TestCase):

    def test_1(self):
        mario0 = LedBitmapObject(Image.open('asset/image/s_mario.png'), 0, 0, 0, 10)
        mario1 = LedBitmapObject(Image.open('asset/image/s_mario_run_1.png'), 0, 0, 0, 10)
        mario2 = LedBitmapObject(Image.open('asset/image/s_mario_run_2.png'), 0, 0, 0, 10)

        self.assertIsNotNone(mario0)
        self.assertIsNotNone(mario1)
        self.assertIsNotNone(mario2)
