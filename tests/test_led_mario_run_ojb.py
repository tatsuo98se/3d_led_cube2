import unittest
from libled.object.led_mario_run_obj import LedMarioRunObject

class TestLedMarioRunObject(unittest.TestCase):

    def test_1(self):
        target = LedMarioRunObject(0)

        self.assertIsNotNone(target)
