from icecream import ic
import re
import os
from colorama import Fore, Style
import jinja2
from .image import MajiboImage

class Shortcodes:

	def __init__(self, root_folder, project, config):
		project_path = os.path.join(root_folder, 'projects', project)

		self.root_folder = root_folder
		self.project = project
		self.project_path = project_path
		self.project_content_path = os.path.join(project_path, 'content')
		self.config = config

	def get_shortcodes(self, text):
		shortcodes = []
		for shortcode in re.findall(r'.*({{([a-z_-]+)\s+([^}]+)}}).*', text):
			arguments = []
			for argument in re.findall(r'\"[^\"]+\"|[^\s]+', shortcode[2].strip()):
				arguments.append(argument.strip().strip('"').strip('\''))
				
			shortcodes.append({
				'shortcode': shortcode[0],
				'tag': shortcode[1],
				'arguments': arguments})
		return shortcodes
	
	def get_embed_arguments(self, shortcode):

		ratio = '16x9'
		url = None

		for argument in shortcode['arguments']:
			argument = argument.strip()
			if re.match(r'[0-9]{1,2}x[0-9]{1,2}', argument):
				ratio = argument
			if shortcode['tag'] == 'iframe' and (argument[0:4] == 'http' or argument[0:4] == '//'):
				url = argument
			if shortcode['tag'] == 'youtube':
				url = f'https://www.youtube.com/embed/{argument}'
				if len(argument)>11:
					url = f'https://www.youtube.com/embed/videoseries?list={argument}'
		
		if url is None:
			print(Fore.RED + f'No "url" in shortcode: "{shortcode["shortcode"]}"' + Style.RESET_ALL)
		
		return {
			'tag': shortcode['tag'],
			'ratio': ratio,
			'url': url,
		}


	def convert(self, text):

		# setup jinja
		templateLoader = jinja2.FileSystemLoader(searchpath=os.path.join(self.root_folder, 'majibo', 'template'))
		templateEnv = jinja2.Environment(loader=templateLoader)

		# setup MajiboImage
		mimg = MajiboImage(self.root_folder, self.project)

		for shortcode in self.get_shortcodes(text):

			# include MD file
			if shortcode['tag'] == 'include':
				include_file = shortcode['arguments'][0] + '.md'
				include_file_path = os.path.join(self.project_content_path, 'include', include_file)

				try:
					fp = open(include_file_path, "r", encoding="utf8")
					include_file_content = fp.read()
					text = text.replace(shortcode['shortcode'], include_file_content)
					fp.close()
				except Exception as ex:
					print(Fore.RED + f'include "include/{include_file}.md": {type(ex).__name__}' + Style.RESET_ALL)
			
			# image
			if shortcode['tag'] == 'image':
				template = templateEnv.get_template('image.html')
				image_title = None
				try:
					image_title = shortcode['arguments'][1].strip()
				except:
					pass

				resized = mimg.resize(shortcode['arguments'][0].strip(), self.config.IMAGE_MAX_WIDTH, False)

				shortcode_html = template.render({
					'file': resized,
					'title': image_title,
					'config': self.config
					})
				text = text.replace(shortcode['shortcode'], shortcode_html)
			
			# gallery
			if shortcode['tag'] == 'gallery':
				template = templateEnv.get_template('gallery.html')
				gallery = []
				for image_file_name in shortcode['arguments']:
					gallery.append({'file': mimg.resize(image_file_name, self.config.IMAGE_GALLERY_MAX_WIDTH, True) })
				
				shortcode_html = template.render({
					'gallery': gallery,
					'config': self.config,
					})
				text = text.replace(shortcode['shortcode'], shortcode_html)
			
			# embed
			if shortcode['tag'] == 'youtube' or shortcode['tag'] == 'iframe':
				template = templateEnv.get_template('embed.html')
				shortcode_html = template.render( self.get_embed_arguments(shortcode) )
				text = text.replace(shortcode['shortcode'], shortcode_html)
			
			if shortcode['tag'] == 'gist':
				template = templateEnv.get_template('gist.html')
				shortcode_html = template.render( {'src': shortcode['arguments'][0].strip()} )
				text = text.replace(shortcode['shortcode'], shortcode_html)
				

				
		return text