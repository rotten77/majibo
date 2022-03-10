import pathlib
import os
from colorama import Fore, Style
import re
import shutil
import jinja2
import markdown
from icecream import ic
from .bootstrap import BootstrapExtension
from .shortcodes import Shortcodes
import importlib.util
from .config_global import *
from datetime import datetime

md = markdown.Markdown(extensions=['meta', BootstrapExtension()])

class Majibo():

	def __init__(self, project, DEVELOPMENT_MODE = False):
		self.root_folder = MAJIBO_ROOT_FOLDER

		project_path = os.path.join(self.root_folder, 'projects', project)
		if os.path.exists(project_path):
			self.project = project
			self.project_path = project_path
			self.project_dist_path = os.path.join(self.root_folder, 'dist', project)
			self.project_template_path = os.path.join(project_path, 'template')
			self.project_content_path = os.path.join(project_path, 'content')
			self.DEVELOPMENT_MODE = DEVELOPMENT_MODE

			print(f'project: {Fore.YELLOW}{project}')
		else:
			print(Fore.RED)
			raise NotADirectoryError(f'Project folder "{project}" not found' + Style.RESET_ALL)
		
		# project config
		try:
			spec = importlib.util.spec_from_file_location("config", os.path.join(project_path, 'config.py'))
			config = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(config)
			self.config = config
		except Exception as ex:
			print(Fore.RED + f'error "{project}/config.py": {type(ex).__name__}' + Style.RESET_ALL)
		
		self.build_project()


	def get_project(self):
		return self.project

	def get_project_content(self):
		project_content = []
		for file in os.listdir(os.path.join(self.project_path, 'content')):
			if re.match('.+\.md', file):
				project_content.append(file.replace('.md', ''))
		return project_content
	
	def get_site_navigation(self, current_file):
		navigation = None
		try:
			navigation = []
			for item in self.config.SITE_NAVIGATION:
				href = LINK_BASE + (f'{item["id"]}.html' if item["id"] != 'index' else '')
				try:
					href = item['href']
				except:
					pass
				navigation.append({
					'id': item['id'],
					'href': href,
					'title': item['title'],
					'is_active': True if current_file == item["id"] else False
				})
		except Exception as ex:
			print(Fore.RED + f'navigation": {type(ex).__name__}' + Style.RESET_ALL)
		return navigation
	
	def build_project(self):
		# create dist folder
		if os.path.exists(self.project_dist_path) and self.DEVELOPMENT_MODE == False:
			shutil.rmtree(self.project_dist_path)
		if not os.path.exists(self.project_dist_path):
			os.makedirs(os.path.join(self.project_dist_path))

		# copy images and assets
		for folder in ['img', 'assets']:
			if not os.path.exists(os.path.join(self.project_dist_path, folder)):
				os.makedirs(os.path.join(self.project_dist_path, folder))
			for file in os.listdir(os.path.join(self.project_path, folder)):
				if not re.match(r'.+\.map', file) and not re.match(r'.+\.scss', file):
					shutil.copyfile(os.path.join(self.project_path, folder, file), os.path.join(self.project_dist_path, folder, file))
		shutil.copyfile(os.path.join(self.root_folder, 'bootstrap', 'js', 'bootstrap.min.js'), os.path.join(self.project_dist_path, 'assets', 'bootstrap.min.js'))
		
		# setup jinja
		templateLoader = jinja2.FileSystemLoader(searchpath=self.project_template_path)
		templateEnv = jinja2.Environment(loader=templateLoader)

		# generate HTML files
		for file in self.get_project_content():
			print()
			print(f'{Fore.CYAN}== {file}.md =========={Style.RESET_ALL}')

			file_path_md = os.path.join(self.project_content_path, f'{file}.md')
			file_path_dist = os.path.join(self.project_dist_path, f'{file}.html')

			# load content
			try:
				fp = open(file_path_md, "r", encoding="utf8")
				markdown_text = fp.read()
				fp.close()
			except Exception as ex:
				print(Fore.RED + f'read "{file}.md": {type(ex).__name__}' + Style.RESET_ALL)

			# shortcodes
			markdown_text = Shortcodes(self.root_folder, self.project, self.config).convert(markdown_text)

			# markdown
			content = md.convert(markdown_text)

			# check default template
			template_file = 'template.html'
			if not os.path.isfile(os.path.join(self.project_template_path, template_file)):
				print(Fore.RED)
				raise FileNotFoundError(f'Template file "{template_file}" not found' + Style.RESET_ALL)

			# set template
			page_template = file
			try:
				page_template = md.Meta['template'][0]
			except:
				pass
			try:
				if os.path.isfile(os.path.join(self.project_template_path, f'{page_template}.html')):
					template_file = f'{page_template}.html'
				else:
					print(Fore.RED + f'template "{page_template}.html" not found' + Style.RESET_ALL)

				template = templateEnv.get_template(template_file)
				print(f'template "{template_file}"')

			except Exception as ex:
				print(Fore.RED + f'template "{template_file}": {type(ex).__name__}' + Style.RESET_ALL)

			# navigation
			navigation = self.get_site_navigation(file)	

			

			# set data for template
			data = {
				'site_language': self.config.SITE_LANG,
				'site_name': self.config.SITE_NAME,
				'site_url': self.config.SITE_URL,
				'site_author': self.config.SITE_AUTHOR,
				'page_url': self.config.SITE_URL + (f'{file}.html' if file !='index' else ''),
				'is_index': (True if file == 'index' else False),
				'page_type': 'website',
				'link_base': LINK_BASE,
				'stylesheet': ((LINK_BASE_ASSETS + 'style.min.css') if self.DEVELOPMENT_MODE == False else f'/projects/{self.project}/assets/style.min.css'),
				'title': None,
				'navigation': navigation,
				'meta': {
					'title': None,
					'image': None,
					'description': None,
				},
            	'content': content
        	}

			 # set metadata
			try:
				data['page_type'] = md.Meta['type'][0]
			except:
				pass

			try:
				data['site_language'] = md.Meta['lang'][0]
			except:
				pass

			try:
				data['title'] = (self.config.SITE_NAME if file == 'index' else md.Meta['title'][0])
				data['meta']['title'] = (self.config.SITE_NAME if file == 'index' else md.Meta['title'][0] + ' &#124; ' + self.config.SITE_NAME)
			except:
				data['meta']['title'] = self.config.SITE_NAME
				print('error during parsing or missing meta "Title" tag')

			try:
				data['meta']['image'] = LINK_BASE_IMG + md.Meta['image'][0]
			except:
				data['meta']['image'] = LINK_BASE_IMG + self.config.PAGE_DEFAULT_IMAGE
				print('error during parsing or missing meta "Image" tag')

			try:
				data['meta']['description'] = md.Meta['description'][0]
			except:
				data['meta']['description'] = self.config.PAGE_DEFAULT_DESCRIPTION
				print('error during parsing or missing meta "Description" tag')

			try:
				data['meta']['author'] = md.Meta['author'][0]
			except:
				print('error during parsing or missing meta "Author" tag')
		
			try:
				data['meta']['date'] = datetime.strptime(md.Meta['date'][0], '%Y-%m-%d %H:%M:%S').strftime(self.config.DATETIME_FORMAT)
			except:
				data['meta']['date'] = datetime.today().strftime(self.config.DATETIME_FORMAT)
				print('error during parsing or missing meta "Date" tag')

			# render
			html = template.render(data)

			# export file
			fp = open(file_path_dist, "w+", encoding="utf8")
			fp.write(html)
			fp.close()
			print(f'exported "{file}.html"')