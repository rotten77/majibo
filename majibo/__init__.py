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
import slug
import urllib.parse

md = markdown.Markdown(extensions=['meta', 'md_in_html', 'tables', 'toc', BootstrapExtension()])

class Majibo():

	def __init__(self, project, DEVELOPMENT_MODE = False, content_file=None):
		self.root_folder = MAJIBO_ROOT_FOLDER
		self.build_timestamp = datetime.today()

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
		
		self.build_project(content_file=content_file)


	def get_project(self):
		return self.project

	def get_project_content(self, content_file):
		project_content = []
		if content_file:
			project_content.append(content_file.replace('\\content\\', '').replace('.md', ''))
		else:
			for file in os.listdir(os.path.join(self.project_path, 'content')):
				if re.match('.+\.md', file):
					project_content.append(file.replace('.md', ''))
		return project_content
	
	def get_site_navigation(self, current_file, navigation_structure=None):
		navigation = None
		navigation_items = navigation_structure if navigation_structure is not None else self.config.SITE_NAVIGATION
		try:
			navigation = []
			for item in navigation_items:
				href = LINK_BASE + (f'{item["id"]}.html' if item["id"] != 'index' else '')
				try:
					href = item['href']
				except:
					pass

				children = None
				try:
					children = self.get_site_navigation(current_file, item['children'])
				except:
					pass
				navigation.append({
					'id': item['id'],
					'href': href,
					'title': item['title'],
					'is_active': True if current_file == item["id"] else False,
					'children': children,
				})
		except Exception as ex:
			print(Fore.RED + f'navigation": {type(ex).__name__}' + Style.RESET_ALL)
		return navigation
	
	def build_project(self,content_file):
		# settings
		try:
			js_bootstrap_package = ('bundle' if self.config.JS_BOOTSTRAP_BUNDLE is True else 'min')
		except:
			js_bootstrap_package = 'min'
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
		shutil.copyfile(os.path.join(self.root_folder, 'bootstrap', 'js', f'bootstrap.{js_bootstrap_package}.js'), os.path.join(self.project_dist_path, 'assets', f'bootstrap.{js_bootstrap_package}.js'))
		shutil.copyfile(os.path.join(self.root_folder, 'bootstrap', 'js', f'bootstrap.{js_bootstrap_package}.js.map'), os.path.join(self.project_dist_path, 'assets', f'bootstrap.{js_bootstrap_package}.js.map'))
		shutil.copyfile(os.path.join(self.root_folder, 'bootstrap', 'bs5-lightbox.js'), os.path.join(self.project_dist_path, 'assets', 'bs5-lightbox.js'))
		shutil.copyfile(os.path.join(self.root_folder, 'bootstrap', 'bs5-lightbox.js.map'), os.path.join(self.project_dist_path, 'assets', 'bs5-lightbox.js.map'))
		
		def urlencode(input):
			return urllib.parse.quote_plus(input)

		# setup jinja
		templateLoader = jinja2.FileSystemLoader(searchpath=self.project_template_path)
		templateEnv = jinja2.Environment(loader=templateLoader)
		templateEnv.filters['urlencode'] = urlencode
		templateEnv.add_extension('jinja2.ext.do')

		# generate HTML files
		for file in self.get_project_content(content_file=content_file):
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

			# add ID to headings
			for heading in re.findall(r'<h([0-9])>([^<]+)', content):
				content = content.replace(f'<h{heading[0]}>{heading[1]}</h{heading[0]}>', f'<h{heading[0]} id="{slug.slug(heading[1])}">{heading[1]}</h{heading[0]}>')

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

				template = templateEnv.get_template(template_file)
				print(f'template "{template_file}"')

			except Exception as ex:
				print(Fore.RED + f'template "{template_file}": {type(ex).__name__}' + Style.RESET_ALL)

			# navigation
			navigation = self.get_site_navigation(file)

			# set data for template
			data = {
				'site': {
					'name': self.config.SITE_NAME,
					'url': self.config.SITE_URL,
					'email': self.config.SITE_EMAIL,
					'author': {
						'name': self.config.SITE_AUTHOR,
						'url':  self.config.SITE_AUTHOR_URL,
						'email':  self.config.SITE_AUTHOR_EMAIL,
					},
					'navigation': navigation,
					'description': self.config.SITE_DESCRIPTION,
					'generator': {
						'name': 'Majibo',
						'url': MAJIBO_URL,
						'version': MAJIBO_VERSION
					},
					'build_id': self.build_timestamp.strftime('%Y%m%d%H%M%S'),
				},
				'page': {
					'url': self.config.SITE_URL + (f'{file}.html' if file !='index' else ''),
					'id': file,
					'template': template_file[:-5],
					'is_index': (True if file == 'index' else False),
					'type': 'website',
					'language': self.config.SITE_LANG,
					'title': None,
					'description': self.config.PAGE_DEFAULT_DESCRIPTION,
					'image': self.config.SITE_URL + 'img/' + self.config.PAGE_DEFAULT_IMAGE,
					'author': self.config.SITE_AUTHOR,
					'content': content
				},
				'link_base': LINK_BASE,
				'assets': {
					'base': LINK_BASE_ASSETS,
					'stylesheet': ((LINK_BASE_ASSETS + 'style.min.css') if self.DEVELOPMENT_MODE == False else f'/projects/{self.project}/assets/style.min.css'),
					'bootstrap': {
						'js': f'{LINK_BASE_ASSETS}bootstrap.{js_bootstrap_package}.js',
						'lightbox': {
							'js': f'{LINK_BASE_ASSETS}bs5-lightbox.js'
						}
					}
				},
				'meta': None
        	}

			# set metadata
			try:
				data['page']['type'] = md.Meta['type'][0]
			except:
				pass

			try:
				data['page']['language'] = md.Meta['lang'][0]
			except:
				pass

			try:
				data['page']['title'] = md.Meta['title'][0]
			except:
				print('error during parsing or missing meta "Title" tag (as page_title)')

			try:
				data['page']['image'] = self.config.SITE_URL + 'img/' + md.Meta['image'][0]
			except:
				data['page']['image'] = self.config.SITE_URL + 'img/' + self.config.PAGE_DEFAULT_IMAGE
				print('error during parsing or missing meta "Image" tag')

			try:
				data['page']['description'] = md.Meta['description'][0]
			except:
				data['page']['description'] = self.config.PAGE_DEFAULT_DESCRIPTION
				print('error during parsing or missing meta "Description" tag')

			try:
				data['page']['author'] = md.Meta['author'][0]
			except:
				pass

			# original meta
			try:
				data['page']['meta'] = md.Meta
			except:
				pass

			# render
			html = template.render(data)

			# export file
			fp = open(file_path_dist, "w+", encoding="utf8")
			fp.write(html)
			fp.close()
			print(f'exported "{file}.html"')