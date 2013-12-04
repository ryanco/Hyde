import unittest
import os
from Hyde import Hyde, Config, CommandArgumentError
from TestUtility import TestUtility, MockArguments


class PublishPostTest(unittest.TestCase, Hyde):

	def test_publish_draft_post(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['draft', 'post', 'A Draft Post To Publish'])
		Hyde.main()
		actual_title = TestUtility.build_jekyll_post_title('a-draft-post-to-publish') + '.md'
		actual_file = Config.posts_drafts_dir + actual_title
		self.assertTrue(os.path.exists(Config.posts_drafts_dir))
		self.assertTrue(os.path.isfile(actual_file))
		os.mkdir(Config.posts_dir)
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['publish', 'A Draft Post To Publish'])
		Hyde.main()
		self.assertTrue(os.path.exists(Config.posts_dir))
		self.assertTrue(os.path.isfile(Config.posts_dir+actual_title))
		TestUtility.remove_directory(Config.posts_dir)
		TestUtility.remove_directory(Config.posts_drafts_dir)
		TestUtility.remove_directory(Config.drafts_dir)
		self.assertFalse(os.path.exists(Config.posts_dir))
		self.assertFalse(os.path.exists(Config.posts_drafts_dir))
		self.assertFalse(os.path.exists(Config.drafts_dir))
		TestUtility.clear_sys_args()

	def test_draft_directory_not_found(self):
		with self.assertRaises(CommandArgumentError) as err:
			TestUtility.append_sys_args(['publish', 'A Draft Post To Publish'])
			Hyde.main()
		self.assertEqual(err.exception.msg, "The drafts directory _drafts/posts/ does not exist.")

	def test_draft_not_found(self):
		TestUtility.clear_sys_args()
		os.mkdir(Config.drafts_dir)
		os.mkdir(Config.posts_drafts_dir)
		with self.assertRaises(CommandArgumentError) as err:
			TestUtility.append_sys_args(['publish', 'A Draft Post To Publish'])
			Hyde.main()
		self.assertEqual(err.exception.msg, "No draft found with 'A-Draft-Post-To-Publish' in the title.")
		TestUtility.remove_directory(Config.drafts_dir)
		self.assertFalse(os.path.exists(Config.drafts_dir))
		TestUtility.clear_sys_args()

	def test_handle_argument_error(self):
		with self.assertRaises(CommandArgumentError) as err:
			args = MockArguments(sub_command='unknown')
			Hyde._handle_publish(args)
		self.assertEqual(err.exception.msg, "The 'publish' sub-command requires a title.")


if __name__ == '__main__':  # pragma: no cover
	unittest.main()
