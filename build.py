from majibo import Majibo
import argparse
import majibo.config_global as config_global
from colorama import Fore, Style

parser = argparse.ArgumentParser()
parser.add_argument('-p', help="project")
parser.add_argument('-d', help="development mode", action="store_true")
parser.add_argument('-v', help="print version", action="store_true")
args = parser.parse_args()


if args.v:
	config_global.about()

if args.p:

	if args.d:
		print(f'Development mode: {Fore.GREEN}on{Style.RESET_ALL}')
		DEVELOPMENT_MODE = True
	else:
		print(f'Development mode: {Fore.RED}off{Style.RESET_ALL}')
		DEVELOPMENT_MODE = False

	Majibo(args.p, DEVELOPMENT_MODE)