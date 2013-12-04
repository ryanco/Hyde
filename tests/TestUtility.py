import sys
import datetime
import os
import shutil


class TestUtility:

	def __init__(self):# pragma: no cover
		pass

	@staticmethod
	def clear_sys_args():
		"""
		Clear the sys.argv list.
		"""
		while len(sys.argv) > 1:
			sys.argv.pop()

	@staticmethod
	def append_sys_args(args):
		"""
		Append the arguments to sys.argv.
		@param args: list of items to add to sys.argv.
		"""
		for arg in args:
			sys.argv.append(arg)

	@staticmethod
	def build_jekyll_post_title(title):
		return datetime.date.today().strftime('%Y-%m-%d-'+title)

	@staticmethod
	def remove_file(expected_file):
		"""
		Removes a post file and the directory
		@param expected_file: the file to remove.
		"""
		os.remove(expected_file)

	@staticmethod
	def remove_directory(path):
		"""
		Remove the directory in the path.
		@param path: the path of a directory that should be removed.
		"""
		shutil.rmtree(path)


class MockArguments(object):
	def __init__(self, sub_command=None, add_item_type=None, draft_item_type=None, title=None):
		self.sub_command = sub_command
		self.add_item_type = add_item_type
		self.draft_item_type = draft_item_type
		self.title = title

