from src.config import Config


def str_to_bool(txt: str):
    if txt.lower() == "true":
        return True
    return False


def get_mc_folder() -> str:
    """Return the minecraft folder from config if found

    Returns:
        str: the mc_folder folder
    """
    conf = Config()
    return conf.read_conf().get("minecraft").get("folder")
