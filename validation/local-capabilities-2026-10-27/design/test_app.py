import unittest
from app import normalize_title

class TestTitle(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(normalize_title("title"), "title")
