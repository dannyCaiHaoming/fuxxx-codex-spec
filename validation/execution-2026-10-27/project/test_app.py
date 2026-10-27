import unittest
from app import parse_tags


class Tags(unittest.TestCase):
    def test_single(self):
        self.assertEqual(parse_tags("a"), ["a"])

    def test_original_input_preserves_order_and_duplicates(self):
        self.assertEqual(parse_tags(" b, a, b, ,"), ["b", "a", "b"])

    def test_empty_items(self):
        for text in ("", " , , ", "\t,\n"):
            with self.subTest(text=text):
                self.assertEqual(parse_tags(text), [])

    def test_trim_without_changing_content(self):
        self.assertEqual(parse_tags(" A B , a;b, A B "), ["A B", "a;b", "A B"])
