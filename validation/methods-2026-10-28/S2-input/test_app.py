import unittest
from app import parse_tags
class Tags(unittest.TestCase):
    def test_single(self):
        self.assertEqual(parse_tags("a"), ["a"])
