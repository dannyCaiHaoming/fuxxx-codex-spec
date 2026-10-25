import unittest, tempfile
from pathlib import Path
from app import add_task, list_tasks
class Tasks(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tasks.json'
   self.assertEqual(list_tasks(p), [])
   a=add_task(p,' 中文任务 '); b=add_task(p,'second')
   self.assertEqual(a['title'],'中文任务'); self.assertNotEqual(a['id'],b['id'])
   self.assertEqual(list_tasks(p),[a,b])
 def test_blank(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tasks.json'
   with self.assertRaises(ValueError): add_task(p,'  ')
   self.assertFalse(p.exists())
if __name__=='__main__': unittest.main()
