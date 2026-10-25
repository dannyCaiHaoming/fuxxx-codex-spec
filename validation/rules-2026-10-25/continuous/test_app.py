import unittest, tempfile
from pathlib import Path
from app import add_task, list_tasks
class Tasks(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as t:
   p=Path(t)/'tasks.json'
   self.assertEqual(list_tasks(p), [])
   a=add_task(p,' 中文任务 '); b=add_task(p,'second')
   self.assertEqual(a['title'],'中文任务'); self.assertNotEqual(a['id'],b['id'])
   self.assertEqual(list_tasks(p),[a,b])
 def test_blank(self):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as t:
   p=Path(t)/'tasks.json'
   with self.assertRaises(ValueError): add_task(p,'  ')
   self.assertFalse(p.exists())

class Persistence(unittest.TestCase):
 def test_blank_preserves_existing_file(self):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as t:
   p=Path(t)/'tasks.json'
   add_task(p,'保留')
   before=p.read_bytes()
   with self.assertRaises(ValueError): add_task(p,' \t\n ')
   self.assertEqual(p.read_bytes(),before)

 def test_reopen_in_new_process(self):
  import json, subprocess, sys
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as t:
   p=Path(t)/'tasks.json'
   first=add_task(p,' 中文任务 ')
   self.assertIn('中文任务',p.read_bytes().decode('utf-8'))
   result=subprocess.run(
    [sys.executable,'-B','-c',
     'import json,sys; from app import add_task,list_tasks; '
     'add_task(sys.argv[1],"重新打开"); print(json.dumps(list_tasks(sys.argv[1])))',str(p)],
    cwd=Path(__file__).parent,capture_output=True,text=True,check=True)
   tasks=json.loads(result.stdout)
   self.assertEqual(tasks[0],first)
   self.assertEqual(tasks[1]['title'],'重新打开')
   self.assertNotEqual(tasks[0]['id'],tasks[1]['id'])
   self.assertEqual(list_tasks(p),tasks)

if __name__=='__main__': unittest.main()
