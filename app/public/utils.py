from src.config import Config
from public.constants import CONFIG_FILE
import os


def str_to_bool(txt: str) -> bool:
    """Convert a string to boolean

    Args:
        txt (str): string

    Returns:
        bool: the converted string
    """
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


def is_def(string: str, match_case: bool = False) -> bool:
    """Checks if a string is a default instance

    Args:
        string (str): name
        match_case (bool, optional): if to match the cases. Defaults to False.

    Returns:
        bool: if it is a default instance
    """
    if not match_case:
        string = string.lower()
    if string.lower() in ["none", "default"]:
        return True
    return False
