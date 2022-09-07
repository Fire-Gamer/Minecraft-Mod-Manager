from src.utils import *
from public.constants import *
from src.instanceManager import InstanceManager
from src.config import Config
import argparse
import os
os.system("")

# TODO better var names and docs

def arguments():
	parser = argparse.ArgumentParser(description="Manage your minecraft mods using this CLI", usage="%(prog)s [options]")
	subparser = parser.add_subparsers()
	create = subparser.add_parser('create', help="Creates a new instance with specified arguments")
	create.add_argument('name', type=str, help="name of instance that is going to be created")
	create.add_argument('settings', choices=["true", "false"], help="weather to save settings file or not")
	create.add_argument('version', type=str, help="MC version to be saved")
	create.add_argument('loader', choices=["fabric", "forge", "vanilla"], help="Loader type")
	lst = subparser.add_parser('list', help="Lists all the available instances")
	lst.add_argument("-m", choices=["s", "f"], help="Mode to be used to list the instances")
	apply = subparser.add_parser('apply', help="Applies the specified instance to mods folder")
	apply.add_argument("name", help="name of an instance")

	args = parser.parse_args()
	return args

def create_dirs():
	if not(os.path.exists(MMMF)): os.makedirs(MMMF)
	if not(os.path.exists(CONFIG_FOLDER)): os.makedirs(CONFIG_FOLDER)
	if not(os.path.exists(INSTANCES_FOLDER)): os.makedirs(INSTANCES_FOLDER)
	if not(os.path.exists(DIF)): os.makedirs(DIF)	
	if not os.path.exists(INDEX):
		with open(INDEX, "w") as index: pass
	if not os.path.exists(CONFIG_FILE):
		with open(CONFIG_FILE, "w") as conf:
				for i in DC:
					conf.write(i)
		


def main():
	# conf = config()
	# if conf.get("run").get("first"):
	# 	pass
		# firstRun()
	if not(os.path.exists(DMF)):
			print("Your minecraft folder can't be found!")
	else:
		try:
			args = arguments()
			mode = get_mode(args)
			instances = []
			create_dirs()
			with open(INDEX, "r") as index:
				for instance in index.readlines():
					instances.append(instance.strip())
			instanceManager = InstanceManager(instances)

			if mode == "create":
				instanceManager.create_instance(args.name,
										True if args.settings == "true" else False, 
										args.version, 
										args.loader)
			if mode == "list":
				details = {}
				for instance in instances:
					detail = {'loader': instanceManager.read_instance(instance).get('loader'), 
					'version': instanceManager.read_instance(instance).get('version')}
					details.update({instance: detail})
				print_instances(instances, details)
		# except Exception as e:
		# 	print(f"[EXCEPTION] [ERROR] {e}")
		finally:
			pass

if __name__ == "__main__":
	main()