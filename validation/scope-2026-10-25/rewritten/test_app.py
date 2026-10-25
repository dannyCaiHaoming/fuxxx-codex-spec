import csv
import tempfile
import unittest
from pathlib import Path

from app import export_csv


class Export(unittest.TestCase):
    def test_roundtrip(self):
        rows = [['中文', 'a,b', 'a"b', 'a\nb'], ['', '\r\n', '末行'], []]
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / 'export.csv'
            export_csv(path, rows)
            with path.open(encoding='utf-8', newline='') as source:
                self.assertEqual(list(csv.reader(source)), rows)

    def test_replace_empty(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = Path(directory) / 'export.csv'
            export_csv(path, [['old']])
            export_csv(path, [])
            self.assertEqual(path.read_bytes(), b'')

    def test_absolute_path_and_replace(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            path = (Path(directory) / 'export.csv').resolve()
            self.assertTrue(path.is_absolute())
            export_csv(str(path), [['old', 'long content'], ['extra']])
            rows = [['新']]
            export_csv(str(path), rows)
            with path.open(encoding='utf-8', newline='') as source:
                self.assertEqual(list(csv.reader(source)), rows)


if __name__ == '__main__':
    unittest.main()
