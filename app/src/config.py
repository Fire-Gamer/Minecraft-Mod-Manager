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
		conf.get("")
		setting = setting_to_str(change) # saves.mc.yea==false
		val = list(change.keys())[0]
		# print(list(change.keys())[0])
		# print(list(change.get(list(change.keys())[0]).items()))
		#! I don't understand this mess
		#! My code will hurt you eyes
		if ((val in [i[0] for i in conf.items()]) 
      		and (list(change.get(val).items())[0][0] in 
           	[i[0] for i in list(conf.get(val).items())])):
			txt = conf_to_str(conf) # [saves] .mc.yea==true [run] fuck
			for i in txt:
				print(i, end="")
			for i in txt:
				if i.find(f"{val}.{setting.split('==')[0]}") != -1:
					index_setting = txt.index(i)
					txt[index_setting] = f'\t{setting}\n'
			for i in txt:
				print(i, end="")
		elif list(change.keys())[0] :
			for i in "txt":
				if (index := i.find(f"[{list(change.keys())[0]}]")) != -1:
					before = [line.strip() for line in txt[:index+1]]
					print(before)
def first_run():
	config("w", {"run", {"first": "false"}})		
	

def conf_to_str(conf: dict) -> list:
	txt_list = []
	for key, value in conf.items():
		txt_list.append(f"[{key}]\n")
		if isinstance(value, dict):
			for i, j in value.items():
				txt_list.append(f"\t{key}.{i}=={j}\n")
	return txt_list

def setting_to_str(setting: dict) -> str:
	for key, value in setting.items():
		for i, j in value.items():
			return f"{i}=={f'{key}.{j}' if j.find(key) != -1 else j}"