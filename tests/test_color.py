import unittest
from libled.util.color import *

class TestColor(unittest.TestCase):

    def test_color_init(self):
        target = Color(1,0.5,0.2)
        self.assertEqual(1.0, target.r)
        self.assertEqual(0.5, target.g)
        self.assertEqual(0.2, target.b)

    def test_color_init2(self):
        target = Color(1,1,1,0.5)
        actual = int(target)
        self.assertEqual(0x808080, actual)
        

    def test_color_init_overrange(self):
        target = Color(-1,1.1,-0.1)
        self.assertEqual(0.0, target.r)
        self.assertEqual(1.0, target.g)
        self.assertEqual(0.0, target.b)

    def test_color_intcast(self):
        target = Color(1,1,1)
        self.assertEqual(0xffffff, int(target))

    def test_color_init_with_tpple(self):
        target = Color.rgbtapple_to_color((1,1,1))
        self.assertEqual(0xffffff, int(target))
        