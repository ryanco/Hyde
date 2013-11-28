import os
import datetime
import unittest
from Hyde import Hyde, DuplicatePostError
from TestUtility import TestUtility


class JekyllPostTest(unittest.TestCase):
	"""
	Tests adding a post and ensures the file is created.
	Then cleans up the file and the directory.
	"""

	def test_handle_add_post(self):
		post_title = 'a test title'
		path = '_posts/'
		Hyde._handle_add_post(post_title, path)
		actual_title = TestUtility.build_jekyll_post_title('a-test-title') + '.md'
		actual_file = path + actual_title
		self.assertTrue(os.path.exists(path))
		self.assertTrue(os.path.isfile(actual_file))
		expected_post_contents = JekyllPostTest.get_expected_post_contents(post_title)
		actual_post_contents = JekyllPostTest.get_actual_post_contents(actual_file)
		self.assertEqual(expected_post_contents, actual_post_contents)
		TestUtility.remove_file(actual_file)
		self.assertFalse(os.path.isfile(actual_file))
		TestUtility.remove_directory(path)
		self.assertFalse(os.path.exists(path))

	def test_handle_add_duplicate_post(self):
		post_title = 'a test title'
		Hyde._handle_add_post(post_title)
		path = '_posts/'
		actual_title = TestUtility.build_jekyll_post_title('a-test-title') + '.md'
		actual_file = path + actual_title
		self.assertTrue(os.path.exists(path))
		self.assertTrue(os.path.isfile(actual_file))
		with self.assertRaises(DuplicatePostError) as err:
			Hyde._handle_add_post(post_title)

		self.assertEqual("The file " + path + actual_title + " already exists. Nothing Created.", err.exception.msg)
		TestUtility.remove_file(actual_file)
		self.assertFalse(os.path.isfile(actual_file))
		TestUtility.remove_directory(path)
		self.assertFalse(os.path.exists(path))

	def test_create_jekyll_post_title(self):
		"""
		Tests the creation of Jekyll post title using the Jekyll format.
		"""
		actual_title = Hyde.create_jekyll_post_title('title for this unit test')
		expected_title = TestUtility.build_jekyll_post_title('title-for-this-unit-test')
		self.assertEquals(expected_title, actual_title)

	@staticmethod
	def get_expected_post_contents(post_title):
		"""
		Creates a post template list for testing.
		@param post_title: the title of the post.
		@return: the expected post template list.
		"""
		expected_post = ['---\n', 'layout: post\n', 'title: ' + post_title + '\n',
						 'date: ' + str(datetime.date.today()) + '\n', '---\n']

		return expected_post

	@staticmethod
	def get_actual_post_contents(post_file):
		"""
		Reads and returns the contents of a post file.
		@param post_file: the post file to read.
		@return: post file contents as a list of lines.
		"""
		with open(post_file) as post_file:
			actual_file = post_file.readlines()

		return actual_file


if __name__ == '__main__':  # pragma: no cover
	unittest.main()
