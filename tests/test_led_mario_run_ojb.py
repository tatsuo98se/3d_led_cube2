import unittest
from libled.object.led_mario_run_obj import LedMarioRunObject
from PIL import Image

class TestLedMarioRunObject(unittest.TestCase):

    def test_1(self):
        target = LedMarioRunObject(0)

        self.assertIsNotNone(target)
