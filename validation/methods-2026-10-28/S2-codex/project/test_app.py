import unittest
from app import parse_tags
class Tags(unittest.TestCase):
    def test_single(self):
        self.assertEqual(parse_tags("a"), ["a"])

    def test_preserves_order_and_duplicates(self):
        self.assertEqual(parse_tags(" b, a, b, ,"), ["b", "a", "b"])

    def test_empty_items(self):
        for text in ("", " \t\n", ",,,", " , \t,\n,"):
            with self.subTest(text=text):
                self.assertEqual(parse_tags(text), [])

    def test_whitespace_and_case(self):
        self.assertEqual(parse_tags(" A ,\tb\n, A, a "), ["A", "b", "A", "a"])

    def test_only_english_comma_separates(self):
        self.assertEqual(parse_tags("a;b,c，d,two words"), ["a;b", "c，d", "two words"])
