import unittest
from libled.util.led_block_util import *

class TestLedBlockUtil(unittest.TestCase):

    # get_blocks_in_loop

    def test_get_blocks_in_loop_1(self):

        orders = ["test","ctrl-1","test2","ctrl-1","test"]

        actual = get_blocks_in_loop(orders, 0)

        self.assertEqual(
            ["test"],
            actual)

    def test_get_blocks_in_loop_2(self):

        orders = ["test","ctrl-1","test2","ctrl-1","test"]

        actual = get_blocks_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)

    def test_get_blocks_in_loop_3(self):

        orders = ["test","ctrl-1","test2","ctrl-1","test"]

        actual = get_blocks_in_loop(orders, 2)

        self.assertEqual(
            ["test2"],
            actual)

    def test_get_blocks_in_loop_4(self):

        orders = ["test","ctrl-1","test2","ctrl-1","test"]

        actual = get_blocks_in_loop(orders, 4)

        self.assertEqual(
            ["test"],
            actual)

    def test_get_blocks_in_loop_5(self):

        orders = ["test","ctrl-1","ctrl-1","test"]

        actual = get_blocks_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)
    # flatten_blocks
    
    def test_flatten_blocks_1(self):

        orders = ["test","ctrl-1","test2","ctrl-1","test"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            ["test", "test2", "test2", "test2", "test"],
            actual)

    def test_flatten_blocks_2(self):

        orders = ["test","ctrl-1","test2","test2","test"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            ["test","test2","test2","test","test2","test2","test","test2","test2","test"],
            actual)

    def test_flatten_blocks_3(self):

        orders = ["test","ctrl-1","ctrl-1","test2","test"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            ["test","test2","test"],
            actual)


    def test_flatten_blocks_4(self):

        orders = ["test","test2","test","test","ctrl-1"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            ["test","test2","test","test"],
            actual)


    def test_flatten_blocks_5(self):

        orders = ["ctrl-1"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_blocks_6(self):

        orders = ["ctrl-1","ctrl-1","ctrl-1","ctrl-1","ctrl-1","ctrl-1"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_blocks_7(self):

        orders = ["ctrl-1","test"]

        actual = flatten_blocks(orders)

        self.assertEqual(
            ["test", "test", "test"],
            actual)