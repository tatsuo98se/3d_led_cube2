import unittest
from libled.util.led_block_util import *
import json

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


    def test_create_block_1(self):
        actual = create_block('object-1', None)
        self.assertTrue(isinstance(actual, LedFillObject))


    def test_create_block_1(self):
        actual = create_block('filter-1', None)
        self.assertTrue(isinstance(actual, LedHsvCanvasFilter))


    def test_json_loads1(self):
        data = "{abc:""}}"
        self.assertRaises(ValueError, json.loads, data)


    def test_json_loads2(self):
        data = '{"abc":"def"}'
        dic = json.loads(data)
        self.assertEqual("def", dic["abc"])
        self.assertRaises(KeyError, dic.__getitem__, "id")


    def test_json_loads3(self):
 #test_data1 = {"filter-2","object-2","object-1","object-2","object-1","filter-0","object-2","object-1"} # this line will be json
        data = """
        {
            "orders":[
                {
                    "id":"filter-2",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-2",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-1",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-2",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-1",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"filter-0",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-1",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                },
                {
                    "id":"object-2",
                    "lifetime":1,
                    "param":{
                        "offset":1
                    }
                }
            ]
        }
        """

        actual = json.loads(data)
        orders = actual['orders']
        self.assertEqual(8, len(orders))
