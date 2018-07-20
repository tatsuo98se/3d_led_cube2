import unittest
from libled.led_cube import *

class TestLedCube(unittest.TestCase):

    def test_local_split_url_and_port_url__only1(self):
        url, port = local_split_url_and_port('aaaa')
        self.assertEqual('aaaa', url)
        self.assertEqual(None, port)

    def test_local_split_url_and_port_url__url_and_port1(self):
        url, port = local_split_url_and_port('aaaa:8080')
        self.assertEqual('aaaa', url)
        self.assertEqual(8080, port)

    def test_local_split_url_and_port_url__only2(self):
        url, port = local_split_url_and_port('192.168.0.3')
        self.assertEqual('192.168.0.3', url)
        self.assertEqual(None, port)

    def test_local_split_url_and_port_url__url_and_port2(self):
        url, port = local_split_url_and_port('192.168.0.3:8080')
        self.assertEqual('192.168.0.3', url)
        self.assertEqual(8080, port)

    def test_local_split_url_and_port__invalid_port__raise_exception(self):
        self.assertRaises(ArgumentError, lambda: local_split_url_and_port('aaaa:aaaa'))

    def test_local_split_url_and_port__invalid_url__raise_exception(self):
        self.assertRaises(ArgumentError, lambda: local_split_url_and_port('aaaa:1234:1234'))