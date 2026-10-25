import unittest
from normalize import normalize_title
from render import render_title
class Tools(unittest.TestCase):
 def test_normalize(self):
  self.assertEqual(normalize_title(' 中文 '),'中文')
  with self.assertRaises(ValueError): normalize_title(' ')
 def test_render(self):
  self.assertEqual(render_title('<a title="x">&'), '&lt;a title=&quot;x&quot;&gt;&amp;')
  self.assertNotIn("'",render_title("'"))
