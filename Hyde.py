#!/usr/bin/python
import argparse
import datetime
import os
import copy


class Config(object):
	#DRAFT CONFIG
	drafts_dir = "_drafts/"

	#POST CONFIGURATION
	posts_dir = '_posts/'
	posts_drafts_dir = drafts_dir + 'posts/'
	post_extension = '.md'
	post_template = ['---\n', 'layout: %layout_type%\n', 'title: %post_title%\n', 'date: %post_date%\n', '---\n']

	#PAGE CONFIGURATION
	new_page_file_name = 'index.md'
	page_template = ['---\n', 'layout: %layout_type%\n', 'title: %page_title%\n', '---\n']


class Hyde():
	VERSION = '1.0.0.0'

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
		parser = argparse.ArgumentParser(prog='Hyde', description='A script for helping with Jekyll tasks.',
										 epilog="Version: " + Hyde.VERSION)
		parser.add_argument('-v', '--version', action='version',
							version="{0}'s version: {1}".format(parser.prog, Hyde.VERSION))

		subparsers = parser.add_subparsers(help='Sub-command for creating Posts or Pages.', dest='sub_command')

		add_command = subparsers.add_parser('add')
		draft_command = subparsers.add_parser('draft')
		publish_command = subparsers.add_parser('publish')
		publish_command.add_argument('title', help='Specify a title for a draft Jekyll post to publish. '
		'The full post name with date is not required.')

		add_command_subparsers = add_command.add_subparsers(dest='add_item_type')
		draft_command_subparsers = draft_command.add_subparsers(dest='draft_item_type')

		# create the parser for the "post" command
		add_post = add_command_subparsers.add_parser('post', help='Create a new Jekyll post.')
		add_post.add_argument('title', help='Specify a title for a new Jekyll post.')
		draft_post = draft_command_subparsers.add_parser('post', help='Create a draft Jekyll post.')
		draft_post.add_argument('title', help='Specify a title for a draft Jekyll post.')

		# create the parser for the "page" command
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
		"""
			Handles the first level sub-command and routes it to the
			matching sub-handler.
			@param args: arguments passed in from the command line or caller.
			@raise CommandArgumentError: argument exception if the sub_command is missing or invalid.
			"""
		if args.sub_command == 'add':
			Hyde._handle_add(args)
		elif args.sub_command == 'draft':
			Hyde._handle_draft(args)
		elif args.sub_command == 'publish':
			Hyde._handle_publish(args)
		else:
			raise CommandArgumentError("No Valid Sub-Command was specified. Expected 'add', 'draft', or 'publish'")


	@staticmethod
	def _handle_add(args):
		"""
			Handle the add sub-command. Determines the item type to add and
			calls the appropriate handler for it.
			@param args: arguments passed into from the command line or caller.
			They should contain the "add_item_type" attribute.
			"""
		if args.add_item_type == 'post':
			Hyde._handle_add_post(args.title)
		elif args.add_item_type == 'page':
			Hyde._handle_add_page(args.title)
		else:
			raise CommandArgumentError("The 'add' sub-command requires a 'post'  or 'page' argument")


	@staticmethod
	def _handle_draft(args):
		"""
			Handle the draft sub-command. Determines the item type to create a draft for and
			calls the appropriate handler for it.
			@param args: arguments passed into from the command line or caller.
			They should contain the "draft_item_type" attribute.
			"""
		if args.draft_item_type == 'post':
			Hyde._handle_add_post(args.title, Config.posts_drafts_dir)
		elif args.draft_item_type == 'page':
			Hyde._handle_add_page(args.title)
		else:
			raise CommandArgumentError("The 'draft' sub-command requires a 'post'  or 'page' argument")


	@staticmethod
	def _handle_publish(args):
		"""
			Handle the publish sub-command. Attempts to find a draft matching the title provided
			and moves it to the posts directory.
			@param args: arguments passed into from the command line or caller.
			They should contain the "title" attribute.
			"""
		if not args.title:
			raise CommandArgumentError("The 'publish' sub-command requires a title.")

		if not os.path.exists(Config.posts_drafts_dir):
			raise CommandArgumentError("The drafts directory %s does not exist." % Config.posts_drafts_dir)

		search_title = Hyde._create_jekyll_title(args.title)
		draft_post_files = os.listdir(Config.posts_drafts_dir)
		for post_file in draft_post_files:
			if search_title in post_file:
				os.rename(Config.posts_drafts_dir + post_file, Config.posts_dir + post_file)
				break
		else:
			raise CommandArgumentError("No draft found with '%s' in the title." % search_title)


	@staticmethod
	def _handle_add_post(title, directory=Config.posts_dir):
		"""
			Creates a Jekyll post using the naming convention and template for Jekyll.
			Writes the files in the configured posts directory.
			@param title: The title of the post.
			"""
		post_file_title = Hyde.create_jekyll_post_title(title)
		posts_directory = directory
		post_extension = Config.post_extension
		post_file_name = post_file_title + post_extension
		if os.path.isfile(posts_directory + post_file_name):
			raise DuplicatePostError("The file " + posts_directory + post_file_name + " already exists. Nothing Created.")
		#create a copy of the template as we are going to customize it.
		post_template = copy.copy(Config.post_template)
		custom_settings = {'%post_title%': title, '%post_date%': str(datetime.date.today()), '%layout_type%': 'post'}
		post_template_content = Hyde.customize_template(custom_settings, post_template)
		Hyde._write_jekyll_file(posts_directory, post_file_name, post_template_content)


	@staticmethod
	def _handle_add_page(page_name):
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
		Hyde._write_jekyll_file(page_path, page_file_name, post_template_content)


	@staticmethod
	def create_jekyll_post_title(title):
		"""
			Creates a Jekyll markdown post title. Using the convention
			that is described here: http://jekyllrb.com/docs/posts/
			@param title: The textual title for the post. (What you expect the user to see on the site).
			@return: the formatted title name following the convention described here: http://jekyllrb.com/docs/posts/
			"""
		date = datetime.date.today()
		return date.strftime('%Y-%m-%d-' + Hyde._create_jekyll_title(title))


	@staticmethod
	def _create_jekyll_title(title):
		"""
			Replaces spaces in a title with dashes. Also ensure the title is not None.
			@param title:
			@return:
			"""
		if not title:
			raise CommandArgumentError("The title cannot be None. Please provide a title.")
		return title.replace(' ', '-')


	@staticmethod
	def _write_jekyll_file(file_path, file_name, content):
		Hyde._create_output_directory(file_path)
		with open(file_path + file_name, "w+") as outfile:
			for line in content:
				outfile.write(line)


	@staticmethod
	def _create_output_directory(path):
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
