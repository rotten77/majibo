from majibo import Majibo
import argparse
import os
import majibo.config_global as config_global
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from consolemenu import SelectionMenu
import webbrowser

# get projects
available_projects = []
for project_name in os.listdir(os.path.join(config_global.MAJIBO_ROOT_FOLDER, 'projects')):
	available_projects.append(project_name)


# arguments parses
parser = argparse.ArgumentParser()
parser.add_argument('-p', help="project", choices=available_projects)
parser.add_argument('-d', help="development mode", action="store_true")
parser.add_argument('-s', help="show exported site", action="store_true")
parser.add_argument('-v', help="print version", action="store_true")
args = parser.parse_args()

# build
if args.v:
	config_global.about()
	exit()

if not args.p:
	args.p = available_projects[SelectionMenu.get_selection(available_projects)]

if args.p:

	project_root = os.path.join(config_global.MAJIBO_ROOT_FOLDER, 'projects', args.p)

	if args.d:
		print(f'Development mode: {Fore.GREEN}on{Style.RESET_ALL}')
		Majibo(args.p, True)

		class MajiboWatchdog(FileSystemEventHandler):
			def on_modified(self, event):
				time.sleep(1)

				modified_file = event.src_path.replace(project_root, '')
				
				try:
					Majibo(args.p, True, content_file=(modified_file if modified_file.startswith('\content') else None))
				except Exception as ex:
					print(f'{Fore.RED}Exception occurred: {ex}{Style.RESET_ALL}')
				
				
				

		observer = Observer()
		observer.schedule(MajiboWatchdog(), path=project_root, recursive=True)
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

		if args.s:
			webbrowser.open(os.path.join(config_global.MAJIBO_ROOT_FOLDER, 'dist', args.p, 'index.html'))