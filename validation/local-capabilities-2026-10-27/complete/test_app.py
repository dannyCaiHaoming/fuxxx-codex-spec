import unittest
from app import normalize_title


class TestTitle(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(normalize_title("title"), "title")

    def test_trim_boundaries(self):
        for title in ("  title  ", "\t\ntitle\r\n", "\u3000title\u00a0"):
            with self.subTest(title=title):
                self.assertEqual(normalize_title(title), "title")

    def test_preserve_internal_whitespace(self):
        for title in ("one  two", "one\ttwo", "one\ntwo"):
            with self.subTest(title=title):
                self.assertEqual(normalize_title("  " + title + "  "), title)

    def test_reject_empty_title(self):
        for title in ("", "   ", "\t\n\r", "\u3000\u00a0"):
            with self.subTest(title=title):
                with self.assertRaises(ValueError) as caught:
                    normalize_title(title)
                self.assertEqual(str(caught.exception), "empty title")
