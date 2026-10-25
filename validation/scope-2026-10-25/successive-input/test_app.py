import csv, tempfile, unittest
from pathlib import Path
from app import export_csv
class Export(unittest.TestCase):
 def test_roundtrip(self):
  rows=[['中文','a,b','a"b','a\nb']]
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'export.csv'; export_csv(p,rows)
   with p.open(encoding='utf-8',newline='') as f: self.assertEqual(list(csv.reader(f)),rows)
 def test_replace_empty(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'export.csv';export_csv(p,[['old']]);export_csv(p,[])
   self.assertEqual(p.read_bytes(),b'')
