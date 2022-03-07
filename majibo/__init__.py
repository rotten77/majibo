import pathlib
import os
from colorama import Fore, Style
import re
import shutil
import jinja2
import markdown
from icecream import ic
from .bootstrap import BootstrapExtension

md = markdown.Markdown(extensions=['meta', BootstrapExtension()])

class Majibo():

	def __init__(self, project):
		self.root_folder = pathlib.Path(__file__).parent.parent.absolute()

		project_path = os.path.join(self.root_folder, 'projects', project)
		if os.path.exists(project_path):
			self.project = project
			self.project_path = project_path
			self.project_dist_path = os.path.join(self.root_folder, 'dist', project)
			self.project_template_path = os.path.join(project_path, 'template')
			self.project_content_path = os.path.join(project_path, 'content')
		else:
			print(Fore.RED)
			raise NotADirectoryError(f'Project folder "{project}" not found' + Style.RESET_ALL)
		
		self.build_project()

	def get_project(self):
		return self.project

	def get_project_content(self):
		project_content = []
		for file in os.listdir(os.path.join(self.project_path, 'content')):
			if re.match('.+\.md', file):
				project_content.append(file.replace('.md', ''))
		return project_content
	
	def build_project(self):
		# create dist folder
		if os.path.exists(self.project_dist_path):
			shutil.rmtree(self.project_dist_path)
		os.makedirs(os.path.join(self.project_dist_path))

		# copy images and assets
		for folder in ['img', 'assets']:
			os.makedirs(os.path.join(self.project_dist_path, folder))
			for file in os.listdir(os.path.join(self.project_path, folder)):
				shutil.copyfile(os.path.join(self.project_path, folder, file), os.path.join(self.project_dist_path, folder, file))
		
		# setup jinja
		templateLoader = jinja2.FileSystemLoader(searchpath=self.project_template_path)
		templateEnv = jinja2.Environment(loader=templateLoader)

		# generate HTML files
		for file in self.get_project_content():
			print(f'== {file}.md ==========')

			file_path_md = os.path.join(self.project_content_path, f'{file}.md')
			file_path_dist = os.path.join(self.project_dist_path, f'{file}.html')

			# check default template
			template_file = 'template.html'
			if not os.path.isfile(os.path.join(self.project_template_path, template_file)):
				print(Fore.RED)
				raise FileNotFoundError(f'Template file "{template_file}" not found' + Style.RESET_ALL)

			# set template
			try:
				if os.path.isfile(os.path.join(self.project_template_path, f'{file}.html')):
					template_file = f'{file}.html'

				template = templateEnv.get_template(template_file)
				print(f'template "{template_file}"')

			except Exception as ex:
				print(Fore.RED + f'template "{template_file}": {type(ex).__name__}' + Style.RESET_ALL)
			
			# load content
			try:
				fp = open(file_path_md, "r", encoding="utf8")
				markdown_text = fp.read()
				fp.close()
			except Exception as ex:
				print(Fore.RED + f'read "{file}.md": {type(ex).__name__}' + Style.RESET_ALL)
			
			# set data for template
			data = {
				'content': md.convert(markdown_text)
			}

			# render
			html = template.render(data)

			# export file
			fp = open(file_path_dist, "w+", encoding="utf8")
			fp.write(html)
			fp.close()
			print(f'exported "{file}.html"')