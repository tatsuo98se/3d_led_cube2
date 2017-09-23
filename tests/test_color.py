import unittest
from libled.util.color import *

class TestColor(unittest.TestCase):

    def test_color_init(self):
        target = Color(1,2,3)
        self.assertEqual(1, target.r)
        self.assertEqual(2, target.g)
        self.assertEqual(3, target.b)

    def test_color_init_overrange(self):
        target = Color(-1,257,-200)
        self.assertEqual(0, target.r)
        self.assertEqual(255, target.g)
        self.assertEqual(0, target.b)

    def test_color_intcast(self):
        target = Color(255,255,255)
        self.assertEqual(0xffffff, int(target))
