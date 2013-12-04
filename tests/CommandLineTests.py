import unittest
from Hyde import Hyde
from TestUtility import TestUtility


class CommandLineTests(unittest.TestCase):

	def test_no_args(self):
		TestUtility.clear_sys_args()
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_unknown_sub_command_no_args(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["unknown"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_unknown_sub_command_valid_post_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["unknown", "post"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_unknown_sub_command_invalid_post_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["unknown", "port"])
		self.verify_system_exit(2)

	def test_unknown_sub_command_invalid_post_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["unknown", "port", "cool title"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_unknown_sub_command_valid_args(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["unknown", "post", "cool title"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_no_args(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["add"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_with_unknown_sub_command_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["add", "unknown"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_with_unknown_sub_command_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["add", "unknown", "cool title"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_post_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["add", "post"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_draft_post_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["draft", "post"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_page_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["add", "page"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_draft_page_no_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(["draft", "page"])
		self.verify_system_exit(2)
		TestUtility.clear_sys_args()

	def test_add_post_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['add', 'post', 'post title'])
		args = Hyde().process_args()
		self.assertEqual("post title", args.title)
		TestUtility.clear_sys_args()

	def test_draft_post_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['draft', 'post', 'draft post title'])
		args = Hyde().process_args()
		self.assertEqual("draft post title", args.title)
		TestUtility.clear_sys_args()

	def test_add_page_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['add', 'page', 'page title'])
		args = Hyde().process_args()
		self.assertEqual("page title", args.title)
		TestUtility.clear_sys_args()

	def test_draft_page_with_title(self):
		TestUtility.clear_sys_args()
		TestUtility.append_sys_args(['draft', 'page', 'draft page title'])
		args = Hyde().process_args()
		self.assertEqual("draft page title", args.title)
		TestUtility.clear_sys_args()

	def verify_system_exit(self, exit_code):
		with self.assertRaises(SystemExit) as cm:
			monkey = Hyde()
			monkey.process_args()
		self.assertEqual(cm.exception.code, exit_code)


if __name__ == '__main__':  # pragma: no cover
	unittest.main()
