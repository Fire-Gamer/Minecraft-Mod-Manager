from src.config import Config
from public.constants import CONFIG_FILE
import os


def str_to_bool(txt: str):
    if txt.lower() == "true":
        return True
    return False


def get_mc_folder() -> str:
    """Return the minecraft folder from config if found

    Returns:
        str: the mc_folder folder
    """
    if os.path.exists(CONFIG_FILE):
        conf = Config()
        if conf.read_conf():
            return conf.read_conf().get("minecraft").get("folder")
    return None
