from ensurepip import bootstrap
import pathlib
from colorama import Fore, Style
import os
import re
from icecream import ic

MAJIBO_VERSION = '0.1.4'
MAJIBO_URL = 'https://majibo.rotten77.cz/'
LINK_BASE = './'
LINK_BASE_IMG = f'{LINK_BASE}img/'
LINK_BASE_ASSETS = f'{LINK_BASE}assets/'
MAJIBO_ROOT_FOLDER = pathlib.Path(__file__).parent.parent.absolute()

# Get bootstrap version
bootstrap_sass_file_path = os.path.join(MAJIBO_ROOT_FOLDER, 'bootstrap', 'scss', 'mixins','_banner.scss')
fp = open(bootstrap_sass_file_path, "r")
bootstrap_sass = fp.read()
fp.close()
bootstrap_findall = re.findall(r'Bootstrap.+([0-9]+\.[0-9]+\.[0-9]+)', bootstrap_sass)
BOOTSTRAP_VERSION = bootstrap_findall[0]

def about():
	print()
	print(Fore.LIGHTBLACK_EX + "* * * * * * * * * * * * * * * * * *")
	print(f'{Fore.YELLOW}MAJIBO {Fore.MAGENTA}v{MAJIBO_VERSION}')
	print()
	print(f'{Style.RESET_ALL}bootstrap version: {Fore.MAGENTA}{BOOTSTRAP_VERSION}')
	print()
	print(f'{Style.RESET_ALL}author: {Fore.MAGENTA}Jan zatloukal')
	print(f'{Fore.CYAN}{MAJIBO_URL}')
	print(Fore.LIGHTBLACK_EX + "* * * * * * * * * * * * * * * * * *")
	print(Style.RESET_ALL)