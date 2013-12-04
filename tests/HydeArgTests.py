import unittest
import os
import shutil
from Hyde import Hyde, CommandArgumentError
from TestUtility import TestUtility, MockArguments


class HydeMainTests(unittest.TestCase):

	NO_VALID_SUB_COMMAND = "No Valid Sub-Command was specified. Expected 'add', 'draft', or 'publish'"
	ADD_MISSING_ARGUMENT = "The 'add' sub-command requires a 'post'  or 'page' argument"
	DRAFT_MISSING_ARGUMENT = "The 'draft' sub-command requires a 'post'  or 'page' argument"
	MISSING_TITLE = "The title cannot be None. Please provide a title."
	MISSING_NAME = "The page name cannot be None. Please provide a page name."

	def test_main_empty_args(self):
		with self.assertRaises(CommandArgumentError) as commandError:
			arguments = MockArguments()
			Hyde.handle_sub_command(arguments)

		self.assertEqual(HydeMainTests.NO_VALID_SUB_COMMAND, commandError.exception.msg)

	def test_main_add_only(self):
		missing_args = MockArguments(sub_command="add")
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.ADD_MISSING_ARGUMENT, commandError.exception.msg)

	def test_main_unknown_sub_command_only(self):
		incorrect_args = MockArguments(sub_command="unknown")
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(incorrect_args)

		self.assertEqual(HydeMainTests.NO_VALID_SUB_COMMAND, commandError.exception.msg)

	def test_main_add_post_no_title(self):
		missing_args = MockArguments(sub_command='add', add_item_type='post')
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.MISSING_TITLE, commandError.exception.msg)

	def test_main_add_unknown_no_title(self):
		incorrect_args = MockArguments(sub_command="add", add_item_type="unknown")
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(incorrect_args)

		self.assertEqual(HydeMainTests.ADD_MISSING_ARGUMENT, commandError.exception.msg)

	def test_main_draft_post_no_title(self):
		missing_args = MockArguments(sub_command='draft', draft_item_type='post')
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.MISSING_TITLE, commandError.exception.msg)

	def test_main_draft_page_no_title(self):
		missing_args = MockArguments(sub_command='draft', draft_item_type='page')
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.MISSING_NAME, commandError.exception.msg)

	def test_main_draft_unknown_no_title(self):
		missing_args = MockArguments(sub_command='draft', draft_item_type='unknown')
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.DRAFT_MISSING_ARGUMENT, commandError.exception.msg)

	def test_main_unknown_unknown_no_title(self):
		missing_args = MockArguments(sub_command='unknown', draft_item_type='unknown')
		with self.assertRaises(CommandArgumentError) as commandError:
			Hyde.handle_sub_command(missing_args)

		self.assertEqual(HydeMainTests.NO_VALID_SUB_COMMAND, commandError.exception.msg)

	def test_main_add_post_with_title(self):
		args = MockArguments(sub_command='add', add_item_type='post', title="real title")
		Hyde.handle_sub_command(args)
		path = '_posts/'
		expected_title = TestUtility.build_jekyll_post_title('real-title') + '.md'
		self.assertTrue(os.path.isfile(path + expected_title))
		os.remove(path + expected_title)
		shutil.rmtree(path)
		self.assertFalse(os.path.isfile(path + expected_title))
		self.assertFalse(os.path.exists(path))

	def test_main_draft_post_with_title(self):
		args = MockArguments(sub_command='draft', draft_item_type='post', title="real title")
		Hyde.handle_sub_command(args)
		path = '_drafts/posts/'
		expected_title = TestUtility.build_jekyll_post_title('real-title') + '.md'
		self.assertTrue(os.path.isfile(path + expected_title))
		os.remove(path + expected_title)
		shutil.rmtree(path)
		self.assertFalse(os.path.isfile(path + expected_title))
		self.assertFalse(os.path.exists(path))

	def test_main_add_page_with_title(self):
		args = MockArguments(sub_command='add', add_item_type='page', title="RealPage")
		Hyde.handle_sub_command(args)
		path = args.title + '/'
		page_file = path + 'index.md'
		self.assertTrue(os.path.isfile(page_file))
		TestUtility.remove_file(page_file)
		self.assertFalse(os.path.isfile(page_file))
		TestUtility.remove_directory(path)
		self.assertFalse(os.path.exists(path))

	def test_process_args_with_args(self):
		input_args = ['add', 'page', "RealPage"]
		args = Hyde.process_args(input_args)
		self.assertEqual(args.sub_command, 'add')
		self.assertEqual(args.add_item_type, 'page')
		self.assertEqual(args.title, "RealPage")

if __name__ == '__main__': # pragma: no cover
	unittest.main()