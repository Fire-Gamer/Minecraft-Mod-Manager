from pathlib import Path
HOME = f"{str(Path.home())}\AppData\Roaming"
MMMF = f"{HOME}\mmm"
CONFIG_FOLDER = f"{MMMF}\\config\\"
INSTANCES_FOLDER = f"{MMMF}\\instances\\"
INDEX = f"{MMMF}\\index"
CONFIG_FILE = f"{CONFIG_FOLDER}config.conf"
DMF = f"{HOME}\.minecraft"
DIF = f"{HOME}\.instances"
DMOF = f"{DMF}\mods"
DC = ["[saves]\n",
		"\tsaves.minecraft.folder==''\n",
		"\tsaves.instance.folder==''\n",
	"[run]\n",
		"\trun.first==true\n",
	"[defaults]\n",
		"\tdefaults.version==None\n",
		"\tdefaults.loader==None\n",
		"\tdefaults.settings==None"]