from icecream import ic
import re
import os
from colorama import Fore, Style

class Shortcodes:

	def __init__(self):
		pass

	def get_shortcodes(self, text):
		shortcodes = []
		for shortcode in re.findall(r'.*({{([a-z_-]+)\s+([^}]+)}}).*', text):
			shortcodes.append({'shortcode': shortcode[0],'tag': shortcode[1], 'arguments': shortcode[2].split(' ')})
		return shortcodes

	def convert(self, text, project_content_path):
		for shortcode in self.get_shortcodes(text):

			# include MD file
			if shortcode['tag'] == 'include':
				include_file = shortcode['arguments'][0] + '.md'
				include_file_path = os.path.join(project_content_path, 'include', include_file)

				try:
					fp = open(include_file_path, "r", encoding="utf8")
					include_file_content = fp.read()
					text = text.replace(shortcode['shortcode'], include_file_content)
					fp.close()
				except Exception as ex:
					print(Fore.RED + f'include "include/{include_file}.md": {type(ex).__name__}' + Style.RESET_ALL)
				
		return text