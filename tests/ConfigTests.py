import unittest
from Hyde import Config


class ConfigTests(unittest.TestCase):
	def test_posts_dir_default(self):
		self.assertEqual("_posts/", Config.posts_dir)

	def test_posts_drafts_dir_default(self):
		self.assertEqual("_drafts/posts/", Config.post_drafts_dir)

	def test_posts_extension_default(self):
		self.assertEqual(".md", Config.post_extension)

	def test_posts_template_default(self):
		self.assertEqual(['---\n', 'layout: %layout_type%\n', 'title: %post_title%\n', 'date: %post_date%\n', '---\n'],
						Config.post_template)

	def test_new_page_file_name_default(self):
		self.assertEqual('index.md', Config.new_page_file_name)

	def test_page_template_default(self):
		self.assertEqual(['---\n', 'layout: %layout_type%\n', 'title: %page_title%\n', '---\n'],
						Config.page_template)