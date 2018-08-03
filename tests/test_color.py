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

    def test_color_init_with_tpple1(self):
        target = Color.rgbtapple_to_color((0xff,0xff,0xff))
        self.assertEqual(0xffffff, int(target))
        self.assertEqual(1.0, target.a)

    def test_color_init_with_tpple2(self):
        target = Color.rgbtapple_to_color((0,0,0))
        self.assertEqual(0, int(target))
        self.assertEqual(1.0, target.a)
                
    def test_int_to_color1(self):
        target = Color.int_to_color(0xffffff)
        self.assertEqual(1.0, target.r)
        self.assertEqual(1.0, target.g)
        self.assertEqual(1.0, target.b)
        self.assertEqual(1.0, target.a)

    def test_int_to_rgbtapple255(self):
        target = Color.int_to_rgbtapple255(0x010203)
        self.assertEqual((1, 2, 3), target)

    def test_rgbtapple255_to_int(self):
        target = Color.rgbtapple255_to_int((1, 2, 3))
        self.assertEqual(0x010203, target)
