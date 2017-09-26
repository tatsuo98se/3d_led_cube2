import unittest
from libled.util.led_block_util import *
import json

class TestLedBlockUtil(unittest.TestCase):

    # get_blocks_in_loop
    test_data = """
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

    def test_get_blocks_in_loop_1(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"ctrl-1"},{"id":"test"}]

        actual = get_blocks_in_loop(orders, 0)

        self.assertEqual(
            [{"id":"test"}],
            actual)

    def test_get_blocks_in_loop_2(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"ctrl-1"},{"id":"test"}]

        actual = get_blocks_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)

    def test_get_blocks_in_loop_3(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"ctrl-1"},{"id":"test"}]

        actual = get_blocks_in_loop(orders, 2)

        self.assertEqual(
            [{"id":"test2"}],
            actual)

    def test_get_blocks_in_loop_4(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"ctrl-1"},{"id":"test"}]

        actual = get_blocks_in_loop(orders, 4)

        self.assertEqual(
            [{"id":"test"}],
            actual)

    def test_get_blocks_in_loop_5(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"test"}]

        actual = get_blocks_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)
    # flatten_blocks
    
    def test_flatten_blocks_1(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"ctrl-1"},{"id":"test"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [{"id":"test"}, {"id":"test2"}, {"id":"test2"}, {"id":"test2"}, {"id":"test"}],
            actual)

    def test_flatten_blocks_2(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"test2"},{"id":"test2"},{"id":"test"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"}],
            actual)

    def test_flatten_blocks_3(self):

        orders = [{"id":"test"},{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"test2"},{"id":"test"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test"}],
            actual)


    def test_flatten_blocks_4(self):

        orders = [{"id":"test"},{"id":"test2"},{"id":"test"},{"id":"test"},{"id":"ctrl-1"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test"},{"id":"test"}],
            actual)


    def test_flatten_blocks_5(self):

        orders = [{"id":"ctrl-1"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_blocks_6(self):

        orders = [{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"ctrl-1"},{"id":"ctrl-1"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_blocks_7(self):

        orders = [{"id":"ctrl-1"},{"id":"test"}]

        actual = flatten_blocks(orders)

        self.assertEqual(
            [{"id":"test"}, {"id":"test"}, {"id":"test"}],
            actual)
            

    def test_create_block_1(self):
        actual = create_block({"id":"object-1"}, None)
        self.assertTrue(isinstance(actual, LedFillObject))


    def test_create_block_1(self):
        actual = create_block({"id":"filter-1"}, None)
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

        actual = json.loads(TestLedBlockUtil.test_data)
        orders = actual['orders']
        self.assertEqual(8, len(orders))

    def test_get_lifetime_from_block_1(self):
        data = {"abc":"def", "lifetime":1}
        self.assertEqual(1, get_lifetime_from_block(data))

    def test_get_lifetime_from_block_2(self):
        data = {"abc":"def"}
        self.assertEqual(5, get_lifetime_from_block(data))

