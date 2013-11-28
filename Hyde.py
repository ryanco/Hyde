#!/usr/bin/python
import argparse
import datetime
import os
import copy


class Config(object):
	#POST CONFIGURATION
	posts_dir = '_posts/'
	post_drafts_dir = '_drafts/posts/'
	post_extension = '.md'
	post_template = ['---\n', 'layout: %layout_type%\n', 'title: %post_title%\n', 'date: %post_date%\n', '---\n']
	#PAGE CONFIGURATION
	new_page_file_name = 'index.md'
	page_template = ['---\n', 'layout: %layout_type%\n', 'title: %page_title%\n', '---\n']


class Hyde():
	def __init__(self):
		pass

	@staticmethod
	def main(args=None):
		"""

		@param args: a list of string arguments.
		@raise MyArgumentError:
		"""
		args = Hyde.process_args(args)
		Hyde.handle_sub_command(args)

	@staticmethod
	def process_args(args=None):
		# create the top-level parser
		"""
		Process and validate the command line arguments.

		@return: args - the validated command line arguments specified.
		"""
		parser = argparse.ArgumentParser(prog='Hyde', description='A script for helping with Jekyll tasks.')
		subparsers = parser.add_subparsers(help='Sub-command for creating Posts or Pages.', dest='sub_command')

		add_command = subparsers.add_parser('add')
		draft_command = subparsers.add_parser('draft')

		add_command_subparsers = add_command.add_subparsers(dest='add_item_type')
		draft_command_subparsers = draft_command.add_subparsers(dest='draft_item_type')

		# create the parser for the "post" command
		add_post = add_command_subparsers.add_parser('post', help='Create a new Jekyll post.')
		add_post.add_argument('title', help='Specify a title for a new Jekyll post.')
		draft_post = draft_command_subparsers.add_parser('post', help='Create a draft Jekyll post.')
		draft_post.add_argument('title', help='Specify a title for a draft Jekyll post.')

		# create the parser for the "post" command
		add_page = add_command_subparsers.add_parser('page', help='Create a new Jekyll page.')
		add_page.add_argument('title', help='Specify a title for a new Jekyll page.')
		draft_page = draft_command_subparsers.add_parser('page', help='Create a draft Jekyll page.')
		draft_page.add_argument('title', help='Specify a title for a draft Jekyll page.')

		if not args:
			args = parser.parse_args()
		else:
			args = parser.parse_args(args)

		return args

	@staticmethod
	def handle_sub_command(args):
		if args.sub_command == 'add':
			Hyde.handle_add(args)
		elif args.sub_command == 'draft':
			Hyde.handle_draft(args)
		else:
			raise CommandArgumentError("No Valid Sub-Command was specified. Expected 'add' or 'draft'")

	@staticmethod
	def handle_add(args):
		"""
		Handle the add sub-command. Determines the item type to add and
		calls the appropriate handler for it.
		@param args: arguments passed into from the command line or caller.
		They should contain the "add_item_type" attribute.
		"""
		if args.add_item_type == 'post':
			Hyde.handle_add_post(args.title)
		elif args.add_item_type == 'page':
			Hyde.handle_add_page(args.title)
		else:
			raise CommandArgumentError("The 'add' sub-command requires a 'post'  or 'page' argument")

	@staticmethod
	def handle_draft(args):
		"""
		Handle the draft sub-command. Determines the item type to create a draft for and
		calls the appropriate handler for it.
		@param args: arguments passed into from the command line or caller.
		They should contain the "draft_item_type" attribute.
		"""
		if args.draft_item_type == 'post':
			Hyde.handle_add_post(args.title, Config.post_drafts_dir)
		elif args.draft_item_type == 'page':
			Hyde.handle_add_page(args.title)
		else:
			raise CommandArgumentError("The 'draft' sub-command requires a 'post'  or 'page' argument")

	@staticmethod
	def handle_add_post(title, directory=Config.posts_dir):
		"""
		Creates a Jekyll post using the naming convention and template for Jekyll.
		Writes the files in the configured posts directory.
		@param title: The title of the post.
		"""
		post_file_title = Hyde.create_jekyll_post_title(title)
		posts_directory = directory
		post_extension = Config.post_extension
		post_file_name = post_file_title + post_extension
		if Hyde.__does_file_exist(posts_directory + post_file_name):
			raise DuplicatePostError("The file " + posts_directory + post_file_name + " already exists. Nothing Created.")
		#create a copy of the template as we are going to customize it.
		post_template = copy.copy(Config.post_template)
		custom_settings = {'%post_title%': title, '%post_date%': str(datetime.date.today()), '%layout_type%': 'post'}
		post_template_content = Hyde.customize_template(custom_settings, post_template)
		Hyde.__write_jekyll_file(posts_directory, post_file_name, post_template_content)

	@staticmethod
	def handle_add_page(page_name):
		"""
		Creates a new page as a directory with an index page. If the page already exists adds a new page with the
		title provided under the existing directory.
		@param page_name: the name for the page.
		"""
		if page_name is None:
			raise CommandArgumentError("The page name cannot be None. Please provide a page name.")
		page_path = page_name + '/'
		page_file_name = Config.new_page_file_name
		#create a copy of the template as we are going to customize it.
		page_template = copy.copy(Config.page_template)
		custom_settings = {'%page_title%': page_name, '%layout_type%': 'page'}
		post_template_content = Hyde.customize_template(custom_settings, page_template)
		Hyde.__write_jekyll_file(page_path, page_file_name, post_template_content)

	@staticmethod
	def create_jekyll_post_title(title):
		"""
		Creates a Jekyll markdown post title. Using the convention
		that is described here: http://jekyllrb.com/docs/posts/
		@param title: The textual title for the post. (What you expect the user to see on the site).
		@return: the formatted title name following the convention described here: http://jekyllrb.com/docs/posts/
		"""
		if title is None:
			raise CommandArgumentError("The title cannot be None. Please provide a title.")
		author_title = title.replace(' ', '-').lower()
		date = datetime.date.today()
		return date.strftime('%Y-%m-%d-' + author_title)

	@staticmethod
	def __write_jekyll_file(file_path, file_name, content):
		Hyde.__create_output_directory(file_path)
		with open(file_path + file_name, "w+") as outfile:
			for line in content:
				outfile.write(line)

	@staticmethod
	def __does_file_exist(file_path_and_name):
		if os.path.isfile(file_path_and_name):
			return True

		return False

	@staticmethod
	def __create_output_directory(path):
		if not os.path.exists(path):
			os.makedirs(path)

	@staticmethod
	def customize_template(custom_values, template):
		"""
		Customizes the template using the passed in custom values dictionary.
		@param custom_values: a dictionary of template keys and replacement values.
		@param template: the template to modify as a list of strings.
		@return: the modified template as a list.
		"""
		for index, line in enumerate(template):
			for key, value in custom_values.iteritems():
				line = line.replace(key, value)
				template[index] = line
		return template


class CommandArgumentError(Exception):
	def __init__(self, msg):
		self.msg = msg


class DuplicatePostError(Exception):
	def __init__(self, msg):
		self.msg = msg


if __name__ == '__main__':  # pragma: no cover
	Hyde.main()
