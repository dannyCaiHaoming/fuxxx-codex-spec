import unittest
from app import parse_tags
class Tags(unittest.TestCase):
    def test_single(self):
        self.assertEqual(parse_tags("a"), ["a"])
    def test_design_input(self):
        self.assertEqual(parse_tags(" b, a, b, ,"), ["b", "a", "b"])
