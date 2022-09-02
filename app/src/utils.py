def print_instances(instances: list, details: dict):
	"""Prints the given instances

	Args:
		instances (list): the list of instances
		details (dict): each detail of instances
	"""
	try:
		len_max = 0
		for instance in instances:
			if len(instance) > len_max: len_max = len(instance)
		len_max += 10
		print(f"\033[4m{'Name':^{len_max}}|{'Version':^16}|{'MC Loader':^16}\033[0m")
		for instance in instances:
			print(f"{instance:^{len_max}}|{details.get(instance).get('version'):^16}|" \
		 		  f"{details.get(instance).get('loader'):^16}")
	except Exception as e:
		print(f"[Error] [Exception] {e}")


def get_mode(args):
	"""Defines mode to use

	Args:
		args (Namespace): the args given

	Returns:
		str: The mode of the run
	"""
	mode = ""
	try:
		if args.name and args.settings and args.loader and args.version: mode = "create"
	except:
		try:
			if args.name: mode = "apply"
		except:
			try:
				if args.m or args.m is None: mode = "list"
			except:
				pass
	return mode

def choose(available: list, prompt: str="", invalid_prompt: str="", default: str=""):
	pmt = f"[{default.lower()}]"
	for i in available:
		if i.lower() != default: pmt += f",{i}"
	if prompt == "" or prompt == None:
		prompt = f"Enter your choice[{pmt}]: "
	if invalid_prompt == "" or invalid_prompt == None:
		invalid_prompt = f"Sorry your choice isn't valid Choose from [{pmt}]: "
	choice = input(prompt)
	if choice.lower() in [i.lower() for i in available]:
		return choice
	else:
		while choice.lower() not in [i.lower() for i in available]:
			choice = input(invalid_prompt)
		return choice