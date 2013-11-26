import unittest
import os
import shutil
from Hyde import Hyde
from TestUtility import TestUtility


class HydeMainTests(unittest.TestCase):

	def test_main_empty_args(self):
		empty_args = []
		self.verify_system_exit(empty_args, 2)

	def test_main_add_only(self):
		missing_args = ['add']
		self.verify_system_exit(missing_args, 2)

	def test_main_unknown_sub_command_only(self):
		missing_args = ['unknown']
		self.verify_system_exit(missing_args, 2)

	def test_main_add_post_no_title(self):
		missing_args = ['add', 'post']
		self.verify_system_exit(missing_args, 2)

	def test_main_add_page_no_title(self):
		missing_args = ['add', 'page']
		self.verify_system_exit(missing_args, 2)

	def test_main_add_unknown_no_title(self):
		missing_args = ['add', 'unknown']
		self.verify_system_exit(missing_args, 2)

	def test_main_draft_post_no_title(self):
		missing_args = ['draft', 'post']
		self.verify_system_exit(missing_args, 2)

	def test_main_draft_page_no_title(self):
		missing_args = ['draft', 'page']
		self.verify_system_exit(missing_args, 2)

	def test_main_draft_unknown_no_title(self):
		missing_args = ['draft', 'unknown']
		self.verify_system_exit(missing_args, 2)

	def test_main_unknown_unknown_no_title(self):
		missing_args = ['unknown', 'unknown']
		self.verify_system_exit(missing_args, 2)


	def test_main_add_post_with_title(self):
		args = ['add', 'post', 'real title']
		Hyde().main(args)
		path = '_posts/'
		expected_title = TestUtility.build_jekyll_post_title('real-title')+'.md'
		self.assertTrue(os.path.isfile(path+expected_title))
		os.remove(path+expected_title)
		shutil.rmtree(path)
		self.assertFalse(os.path.isfile(path+expected_title))
		self.assertFalse(os.path.exists(path))

	def test_main_draft_post_with_title(self):
		args = ['draft', 'post', 'real title']
		Hyde().main(args)
		path = '_drafts/posts/'
		expected_title = TestUtility.build_jekyll_post_title('real-title')+'.md'
		self.assertTrue(os.path.isfile(path+expected_title))
		os.remove(path+expected_title)
		shutil.rmtree(path)
		self.assertFalse(os.path.isfile(path+expected_title))
		self.assertFalse(os.path.exists(path))

	def test_main_add_page_with_title(self):
		args = ['add', 'page', "real title"]
		Hyde().main(args)
		path = args[2] + '/'
		page_file = path+'index.md'
		self.assertTrue(os.path.isfile(page_file))
		TestUtility.remove_file(page_file)
		self.assertFalse(os.path.isfile(page_file))
		TestUtility.remove_directory(path)
		self.assertFalse(os.path.exists(path))
	
	def verify_system_exit(self, args, exit_code):
		with self.assertRaises(SystemExit) as cm:
			Hyde().main(args)

		self.assertEqual(cm.exception.code, exit_code)

if __name__ == '__main__': # pragma: no cover
	unittest.main()