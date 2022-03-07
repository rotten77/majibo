import os
import re
from icecream import ic
from PIL import Image

class MajiboImage():

	def __init__(self, root_folder, project):
		self.root_folder = root_folder
		project_path = os.path.join(self.root_folder, 'projects', project)
		self.project = project
		self.project_path = project_path
		self.project_img_path = os.path.join(project_path, 'img')
		self.project_dist_img_path = os.path.join(self.root_folder, 'dist', project, 'img')

	def resize(self, image_file_name, max_size=800, crop=False):
		image_file_path = os.path.join(self.project_img_path,  image_file_name)
		image_meta_data = None

		if os.path.isfile(image_file_path):

			image = Image.open(image_file_path)

			image_meta_data = {
				'src': image_file_name,
				'width': image.width,
				'height': image.height,
				'thumbnail_src': image_file_name,
				'thumbnail_width': image.width,
				'thumbnail_height': image.height,
			}

			if image.width > max_size or crop == True:
				image_thumbnail_file_name = re.sub('(.+)(\.[a-z]{3,4})', r'\1_thumb\2', image_file_name)

				if crop:
					width, height = image.size   # Get dimensions

					left = (width - max_size)/2
					top = (height - max_size)/2
					right = (width + max_size)/2
					bottom = (height + max_size)/2

					# Crop the center of the image
					image = image.crop((left, top, right, bottom))
					
				image.thumbnail((max_size, max_size))
				image.save(os.path.join(self.project_dist_img_path,  image_thumbnail_file_name))

				image_meta_data['thumbnail_src'] = image_thumbnail_file_name
				image_meta_data['thumbnail_width'] = image.width
				image_meta_data['thumbnail_height'] = image.height
		
		return image_meta_data