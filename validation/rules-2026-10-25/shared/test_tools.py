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

 def test_normalize_empty_and_unicode_whitespace(self):
  for title in ('', ' \t\r\n', '\u3000\u2003'):
   with self.subTest(title=repr(title)):
    with self.assertRaises(ValueError): normalize_title(title)
  self.assertEqual(normalize_title('\u3000中文 内部 空格\u2003'), '中文 内部 空格')

 def test_render_characters_and_preserved_text(self):
  self.assertEqual(render_title("&<>\"'"), '&amp;&lt;&gt;&quot;&#x27;')
  for title in ('', '中文 plain', ' \t中文\n '):
   with self.subTest(title=repr(title)):
    result = render_title(title)
    self.assertEqual(result, title)
    self.assertIsInstance(result, str)
