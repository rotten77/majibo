SITE_LANG = 'en'
SITE_NAME = 'Majibo'
SITE_DESCRIPTION = 'Static site generator written in Python'
SITE_URL = 'https://majibo.rotten77.cz/'
SITE_EMAIL = 'zatloukal.jan@gmail.com'
SITE_AUTHOR = 'Jan Zatloukal'
SITE_AUTHOR_URL = 'https://rotten77.cz/'
SITE_AUTHOR_EMAIL = 'zatloukal.jan@gmail.com'

SITE_NAVIGATION = [
	{'id': 'index', 'title': 'About'},
	{'id': 'configuration', 'title': 'Configuration'},
	{'id': 'content', 'title': 'Content'},
	{'id': 'templates', 'title': 'Templates'},
	{'id': 'example', 'title': 'Example page', 'children': [{'id': 'child-page', 'title': 'Child'}]},
	{'id': 'github', 'href': 'https://github.com/rotten77/majibo', 'title': 'Get Majibo'},
]

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'

PAGE_DEFAULT_IMAGE = 'majibo-forest.png'
PAGE_DEFAULT_DESCRIPTION = 'Majibo is a static site generator written in Python and designed for my personal purposes.'

IMAGE_MAX_WIDTH = 600
IMAGE_GALLERY_THUMBNAIL_SIZE = 240

JS_BOOTSTRAP_BUNDLE = True