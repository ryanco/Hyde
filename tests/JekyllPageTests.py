import os
import unittest
from Hyde import Hyde
from TestUtility import TestUtility


class JekyllPageTest(unittest.TestCase):

	def test_handle_add_new_page(self):
		"""
		Tests adding a page and ensures the file is created.
		Then cleans up the file and the directory.
		"""
		page_name = 'TestPage'
		actual_file_name = 'index.md'
		Hyde._handle_add_page(page_name)
		actual_file = page_name + '/' + actual_file_name
		self.assertTrue(os.path.exists(page_name))
		self.assertTrue(os.path.isfile(actual_file))
		expected_page_contents = JekyllPageTest.get_expected_page_contents(page_name)
		actual_page_contents = JekyllPageTest.get_actual_page_contents(actual_file)
		self.assertEqual(expected_page_contents, actual_page_contents)
		TestUtility.remove_file(actual_file)
		self.assertFalse(os.path.isfile(actual_file))
		TestUtility.remove_directory(page_name)
		self.assertFalse(os.path.exists(page_name))

	def test_handle_add_existing_page(self):
		"""
		Tests adding a page that already exists.
		Ensures a sub-page is created correctly and that
		the existing page remains unchanged.
		"""
		page_name = 'TestPage'
		actual_file_name = 'index.md'
		Hyde._handle_add_page(page_name)
		actual_file = page_name + '/' + actual_file_name
		self.assertTrue(os.path.exists(page_name))
		self.assertTrue(os.path.isfile(actual_file))
		Hyde._handle_add_page(page_name)
		self.assertTrue(os.path.exists(page_name))
		self.assertTrue(os.path.isfile(actual_file))


	@staticmethod
	def get_expected_page_contents(page_name):
		"""
		Creates a post template list for testing.
		@param page_name: the name of the page.
		@return: the expected post template list.
		"""
		expected_page = ['---\n',
			'layout: page\n',
			'title: ' + page_name + '\n',
			'---\n']

		return expected_page

	@staticmethod
	def get_actual_page_contents(page_file):
		"""
		Reads and returns the contents of a post file.
		@param page_file: the page file to read.
		@return: post file contents as a list of lines.
		"""
		with open(page_file) as post_file:
			actual_file = post_file.readlines()

		return actual_file

if __name__ == '__main__':# pragma: no cover
	unittest.main()
