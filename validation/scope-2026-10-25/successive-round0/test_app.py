import csv
import tempfile
import unittest
from pathlib import Path

from app import export_csv


class Export(unittest.TestCase):
    def test_roundtrip(self):
        rows = [["中文", "a,b", 'a"b', "a\nb"], ["", "\r\n", "尾行"], []]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "export.csv"
            self.assertTrue(path.is_absolute())
            export_csv(path, rows)
            with path.open(encoding="utf-8", newline="") as source:
                self.assertEqual(list(csv.reader(source)), rows)

    def test_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            export_csv(path, [])
            self.assertEqual(path.read_bytes(), b"")

    def test_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "export.csv"
            export_csv(path, [["old", "long old content"], ["old row"]])
            export_csv(path, [["新"]])
            with path.open(encoding="utf-8", newline="") as source:
                self.assertEqual(list(csv.reader(source)), [["新"]])
            export_csv(path, [])
            self.assertEqual(path.read_bytes(), b"")
