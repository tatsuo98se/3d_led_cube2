import unittest
from libled.util.led_order_util import *
import json

class TestLedOrderUtil(unittest.TestCase):

    # get_orders_in_loop
    test_data = """
    {
        "orders":[
            {
                "id":"filter-wave",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-ripple",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-fill",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-ripple",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-fill",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"filter-clear",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-fill",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            },
            {
                "id":"object-ripple",
                "lifetime":1,
                "param":{
                    "offset":1
                }
            }
        ]
    }
    """

    def test_get_orders_in_loop_1(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = get_orders_in_loop(orders, 0)

        self.assertEqual(
            [{"id":"test"}],
            actual)

    def test_get_orders_in_loop_2(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = get_orders_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)

    def test_get_orders_in_loop_3(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = get_orders_in_loop(orders, 2)

        self.assertEqual(
            [{"id":"test2"}],
            actual)

    def test_get_orders_in_loop_4(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = get_orders_in_loop(orders, 4)

        self.assertEqual(
            [{"id":"test"}],
            actual)

    def test_get_orders_in_loop_5(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = get_orders_in_loop(orders, 1)

        self.assertEqual(
            [],
            actual)
    # flatten_orders
    
    def test_flatten_orders_1(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"ctrl-loop"},{"id":"test"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [{"id":"test"}, {"id":"test2"}, {"id":"test2"}, {"id":"test2"}, {"id":"test"}],
            actual)

    def test_flatten_orders_2(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"test2"},{"id":"test"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"},{"id":"test2"},{"id":"test2"},{"id":"test"}],
            actual)

    def test_flatten_orders_3(self):

        orders = [{"id":"test"},{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"test2"},{"id":"test"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test"}],
            actual)


    def test_flatten_orders_4(self):

        orders = [{"id":"test"},{"id":"test2"},{"id":"test"},{"id":"test"},{"id":"ctrl-loop"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [{"id":"test"},{"id":"test2"},{"id":"test"},{"id":"test"}],
            actual)


    def test_flatten_orders_5(self):

        orders = [{"id":"ctrl-loop"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_orders_6(self):

        orders = [{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"ctrl-loop"},{"id":"ctrl-loop"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [],
            actual)

    def test_flatten_orders_7(self):

        orders = [{"id":"ctrl-loop"},{"id":"test"}]

        actual = flatten_orders(orders)

        self.assertEqual(
            [{"id":"test"}, {"id":"test"}, {"id":"test"}],
            actual)
            

    def test_create_order_1(self):
        actual = create_order({"id":"object-fill"}, None)
        self.assertTrue(isinstance(actual, LedFillObject))


    def test_create_order_2(self):
        actual = create_order({"id":"filter-hsv"}, None)
        self.assertTrue(isinstance(actual, LedHsvCanvasFilter))


    def test_create_order_3(self):
        actual = create_order({"id":"object-bitmap", "param":{"z":1, "bitmap":"iVBORw0KGgoAAAANSUhEUgAAABAAAAAgCAYAAAAbifjMAAAEDWlDQ1BJQ0MgUHJvZmlsZQAAOI2NVV1oHFUUPrtzZyMkzlNsNIV0qD8NJQ2TVjShtLp/3d02bpZJNtoi6GT27s6Yyc44M7v9oU9FUHwx6psUxL+3gCAo9Q/bPrQvlQol2tQgKD60+INQ6Ium65k7M5lpurHeZe58853vnnvuuWfvBei5qliWkRQBFpquLRcy4nOHj4g9K5CEh6AXBqFXUR0rXalMAjZPC3e1W99Dwntf2dXd/p+tt0YdFSBxH2Kz5qgLiI8B8KdVy3YBevqRHz/qWh72Yui3MUDEL3q44WPXw3M+fo1pZuQs4tOIBVVTaoiXEI/MxfhGDPsxsNZfoE1q66ro5aJim3XdoLFw72H+n23BaIXzbcOnz5mfPoTvYVz7KzUl5+FRxEuqkp9G/Ajia219thzg25abkRE/BpDc3pqvphHvRFys2weqvp+krbWKIX7nhDbzLOItiM8358pTwdirqpPFnMF2xLc1WvLyOwTAibpbmvHHcvttU57y5+XqNZrLe3lE/Pq8eUj2fXKfOe3pfOjzhJYtB/yll5SDFcSDiH+hRkH25+L+sdxKEAMZahrlSX8ukqMOWy/jXW2m6M9LDBc31B9LFuv6gVKg/0Szi3KAr1kGq1GMjU/aLbnq6/lRxc4XfJ98hTargX++DbMJBSiYMIe9Ck1YAxFkKEAG3xbYaKmDDgYyFK0UGYpfoWYXG+fAPPI6tJnNwb7ClP7IyF+D+bjOtCpkhz6CFrIa/I6sFtNl8auFXGMTP34sNwI/JhkgEtmDz14ySfaRcTIBInmKPE32kxyyE2Tv+thKbEVePDfW/byMM1Kmm0XdObS7oGD/MypMXFPXrCwOtoYjyyn7BV29/MZfsVzpLDdRtuIZnbpXzvlf+ev8MvYr/Gqk4H/kV/G3csdazLuyTMPsbFhzd1UabQbjFvDRmcWJxR3zcfHkVw9GfpbJmeev9F08WW8uDkaslwX6avlWGU6NRKz0g/SHtCy9J30o/ca9zX3Kfc19zn3BXQKRO8ud477hLnAfc1/G9mrzGlrfexZ5GLdn6ZZrrEohI2wVHhZywjbhUWEy8icMCGNCUdiBlq3r+xafL549HQ5jH+an+1y+LlYBifuxAvRN/lVVVOlwlCkdVm9NOL5BE4wkQ2SMlDZU97hX86EilU/lUmkQUztTE6mx1EEPh7OmdqBtAvv8HdWpbrJS6tJj3n0CWdM6busNzRV3S9KTYhqvNiqWmuroiKgYhshMjmhTh9ptWhsF7970j/SbMrsPE1suR5z7DMC+P/Hs+y7ijrQAlhyAgccjbhjPygfeBTjzhNqy28EdkUh8C+DU9+z2v/oyeH791OncxHOs5y2AtTc7nb/f73TWPkD/qwBnjX8BoJ98VVBg/m8AAAEVSURBVEgN7VXBDcIwDHQqRmKATsME/Gn/TMA0HYCdis/tpY6VVqC8QFhynNi5i7kmIs1q0mBdA9agzQQndpBS4vSjCNSXa9As4p9A5Ac0yG+BD6B2r49eSfEWamASM0ayQsSxF6HL8yJwrBEBjGBNbV9h6EVudwWpMdpiHWYlgUcrOmBxvD44NTK/jiRZA3QAi6d7MOrDhHGzTMBUPIF5xHTeOmO+IMhdTIuY3BRPZR4x3wOCfRHz26RDr75aJOuQr4EBNPAKZKjtnfV3m2sR/zLLGtHNrbbuUzLcOXPToBCuIpSd7u6AF7Njaxb3wCju1IqvgJ5oKMBquaWyjJnAixOVPqrZT/AbPHttHvfmDmqb38m9APu7aLyM3S4UAAAAAElFTkSuQmCC"}}, None)
        self.assertTrue(isinstance(actual, LedBitmapObject))


    def test_json_loads1(self):
        data = "{abc:""}}"
        self.assertRaises(ValueError, json.loads, data)


    def test_json_loads2(self):
        data = '{"abc":"def"}'
        dic = json.loads(data)
        self.assertEqual("def", dic["abc"])
        self.assertRaises(KeyError, dic.__getitem__, "id")


    def test_json_loads3(self):

        actual = json.loads(TestLedOrderUtil.test_data)
        orders = actual['orders']
        self.assertEqual(8, len(orders))

    def test_get_lifetime_from_order_1(self):
        data = {"abc":"def", "lifetime":1}
        self.assertEqual(1, get_lifetime_from_order(data))

    def test_get_lifetime_from_order_2(self):
        data = {"abc":"def"}
        self.assertEqual(5, get_lifetime_from_order(data))


    def test_get_param_from_order_1(self):
        data = {"id":"test", "param":{"count":1}}
        self.assertEqual(1, get_param_from_order(data, 'count'))

    def test_get_param_from_order_2(self):
        data = {"id":"test"}
        self.assertEqual(None, get_param_from_order(data, 'count'))

