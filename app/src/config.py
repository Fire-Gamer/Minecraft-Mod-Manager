from public.constants import *
import os

def conf_block(start: str, conf: list, end: list = ["[", "]"]) -> list:
	"""Gets a block of config between the start and end

	Args:
		start (str): The start of the block ex: [start]
		conf (list): the config list witch contains all configurations
		end (list, optional): End chars. Defaults to ["[", "]"].

	Returns:
		list: the conf block
	"""
	for i in conf:
		if i.find(end[0]) != -1 and i.find(end[1]) != -1 and i != start and conf.index(i) > conf.index(start):
			return conf[conf.index(start)+1:conf.index(i)]
		else:
			if conf.index(i) == len(conf)-1 and i != start and conf.index(i) > conf.index(start):
				return conf[conf.index(start)+1:conf.index(i)+1]
			
def update_settings(conf):
	"""Updates the settings files

	Args:
		conf (list): the config file

	Returns:
		list: settings that can be added or changed
	"""
	settings = []
	for i in conf:
		if i.find("[") != -1 and i.find("]") != -1:
			settings.append(f"{i}\n")
	return settings


#! May be added parameters change: bool = False, new: bool = False, new_setting: dict = {}
def config(mode: str="r", change: dict = None) -> dict:
	"""Does something to the config file based on the specified mode

	Args:
		mode (str, optional): The mode to be done. Defaults to "r".

	Returns:
		dict: The output based on mode or None if an error occurred
	"""
	modes = ["r","w"]
	if mode.lower() not in modes: return None
	if not os.path.exists(CONFIG_FILE): print(f"[ERROR] [INFO] Config file not found"); return None
	if mode == "r":
		try:
			config_dict = {}
			settings = []
			with open(CONFIG_FILE, "r") as config_read:
				conf = [i.strip() for i in config_read.readlines()]
				for i in update_settings(conf):
					settings.append(i)
					configs = [i.strip() for i in settings]
					for i in configs:
						name = i.replace("[", "").replace("]", "")
						x = {i.replace(f"{name}.", "").split('==')[0]:i.replace(f"{name}.", "").split('==')[1] for i in conf_block(i, conf)}
						config_dict.update({name: x})
		except Exception as e:
			print(f"[ERROR] [EXCEPTION] {e}")
			return None
		else:
			return config_dict
	if mode.lower() == "w" and change is not None:
		conf = config()
		# TODO add the write code
		# print(change.keys())
		# for i,j in conf.items():
		# 	if type(j) == dict:
		# 		print(f"{j}")
		# 		for k, l in j.items:
		# 			print(f"{k}: {l}")
		# 	print(f"{i}: {j}")
			

def conf_to_str(conf) -> str:
	txt = []