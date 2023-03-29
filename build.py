from majibo import Majibo
import argparse
import os
import majibo.config_global as config_global
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# get projects
available_projects = []
for project_name in os.listdir(os.path.join(config_global.MAJIBO_ROOT_FOLDER, 'projects')):
	available_projects.append(project_name)

# arguments parses
parser = argparse.ArgumentParser()
parser.add_argument('-p', help="project", choices=available_projects)
parser.add_argument('-d', help="development mode", action="store_true")
parser.add_argument('-v', help="print version", action="store_true")
args = parser.parse_args()

# build
if args.v:
	config_global.about()

if args.p:

	if args.d:
		print(f'Development mode: {Fore.GREEN}on{Style.RESET_ALL}')
		Majibo(args.p, True)

		class MajiboWatchdog(FileSystemEventHandler):
			def on_modified(self, event):
				try:
					Majibo(args.p, True)
				except Exception as ex:
					print(f'{Fore.RED}Exception occurred: {ex}{Style.RESET_ALL}')
				
				time.sleep(1)
				

		observer = Observer()
		observer.schedule(MajiboWatchdog(), path=os.path.join(config_global.MAJIBO_ROOT_FOLDER, 'projects', args.p), recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(4)
		except KeyboardInterrupt:
			observer.stop()
			observer.join()

	else:
		print(f'Development mode: {Fore.RED}off{Style.RESET_ALL}')
		Majibo(args.p, False)