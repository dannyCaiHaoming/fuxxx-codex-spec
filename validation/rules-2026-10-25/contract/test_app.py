import unittest

from app import normalize_title


class Title(unittest.TestCase):
    def test_accepted_lengths(self):
        for length in (1, 20, 21, 40):
            with self.subTest(length=length):
                title = "中" * length
                self.assertEqual(normalize_title(title), title)

    def test_over_limit_is_rejected(self):
        for title in ("中" * 41, "a" * 80, "  " + "中" * 41 + "  "):
            with self.subTest(length=len(title.strip())):
                with self.assertRaises(ValueError):
                    normalize_title(title)

    def test_strip_precedes_validation(self):
        title = "中" * 40
        self.assertEqual(normalize_title(" \t" + title + "\n "), title)

    def test_blank_is_rejected(self):
        for title in ("", " ", "\t\n", "\u3000"):
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    normalize_title(title)

    def test_internal_whitespace_is_preserved(self):
        self.assertEqual(normalize_title("  a  中  "), "a  中")

    def test_unicode_is_counted_as_python_characters(self):
        title = "😀" * 40
        self.assertEqual(normalize_title(title), title)
        with self.assertRaises(ValueError):
            normalize_title(title + "😀")
