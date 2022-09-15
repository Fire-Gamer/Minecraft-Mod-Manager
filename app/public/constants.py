from pathlib import Path
import os

HOME = f"{str(Path.home())}\AppData\Roaming"
MMMF = f"{HOME}\mmm"
CONFIG_FOLDER = f"{MMMF}\\config\\"
INSTANCES_FOLDER = f"{MMMF}\\instances\\"
INDEX = f"{MMMF}\\index"
CONFIG_FILE = f"{CONFIG_FOLDER}config.conf"
DMF = f"{HOME}\.minecraft"
DIF = f"{HOME}\.instances"
DMOF = f"{DMF}\mods"
DC = [
    "[minecraft]\n",
    "\tminecraft.folder==''\n",
    "[run]\n",
    "\trun.first==true\n",
    "[defaults]\n",
    "\tdefaults.version==None\n",
    "\tdefaults.loader==None\n",
    "\tdefaults.settings==None",
]


def get_paths(conf=None):
    if not conf:
        print(f"Not given a config")
        return None
    paths = {}
    if mc_folder := conf.read_conf().get("minecraft").get("folder"):
        print(mc_folder)
        paths.update({"mc_folder": mc_folder})
    else:
        paths.update({"mc_folder": 0})
    paths.update({".instance": DIF})
    paths.update({".conf": CONFIG_FILE})


# TODO finish and replace with other
