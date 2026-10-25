import unittest, tempfile
import json, subprocess, sys
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
 def test_blank_preserves_existing_file(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tasks.json'
   add_task(p,'保留任务')
   before=p.read_bytes()
   with self.assertRaises(ValueError): add_task(p,' \n\t ')
   self.assertEqual(p.read_bytes(),before)
 def test_reopen_in_new_process(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tasks.json'
   expected=add_task(p,'重新打开')
   self.assertIn('重新打开',p.read_text(encoding='utf-8'))
   result=subprocess.run(
    [sys.executable,'-B','-c',
     'import json,sys; from app import list_tasks; print(json.dumps(list_tasks(sys.argv[1])))',str(p)],
    cwd=Path(__file__).resolve().parent,check=True,capture_output=True,text=True)
   self.assertEqual(json.loads(result.stdout),[expected])
if __name__=='__main__': unittest.main()
