import unittest
from app import parse_tags
class Tags(unittest.TestCase):
    def test_single(self):
        self.assertEqual(parse_tags("a"), ["a"])

    def test_trim_drop_empty_keep_order_and_duplicates(self):
        self.assertEqual(parse_tags(" b, a, b, ,"), ["b", "a", "b"])

    def test_empty_input(self):
        self.assertEqual(parse_tags(""), [])
