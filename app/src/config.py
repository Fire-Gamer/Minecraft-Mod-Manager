from public.constants import CONFIG_FILE, DC, DMF
import os


class Config(object):
    def __init__(self, config_path=CONFIG_FILE):
        if not os.path.exists(config_path):
            print(f"Config file at {config_path} could not be found")
        else:
            self.config_path = config_path
        if self.read_conf().get("run").get("first") == "true":
            self.first_run()

    def conf_block(self, start: str, conf: list, end: list = ["[", "]"]) -> list:
        """Gets a block of config between the start and end

        Args:
                start (str): The start of the block ex: [start]
                conf (list): the config list witch contains all configurations
                end (list, optional): End chars. Defaults to ["[", "]"].

        Returns:
                list: the conf block
        """
        for i in conf:
            if (
                i.find(end[0]) != -1
                and i.find(end[1]) != -1
                and i != start
                and conf.index(i) > conf.index(start)
            ):
                return conf[conf.index(start) + 1 : conf.index(i)]
            else:
                if (
                    conf.index(i) == len(conf) - 1
                    and i != start
                    and conf.index(i) > conf.index(start)
                ):
                    return conf[conf.index(start) + 1 : conf.index(i) + 1]

    def update_settings(self, conf):
        """
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

    def read_conf(self) -> dict:
        try:
            config_dict = {}
            settings = []
            with open(self.config_path, "r") as config_read:
                conf = [i.strip() for i in config_read.readlines()]
                for i in self.update_settings(conf):
                    settings.append(i)
                    configs = [i.strip() for i in settings]
                    for i in configs:
                        name = i.replace("[", "").replace("]", "")
                        x = {
                            i.replace(f"{name}.", "")
                            .split("==")[0]: i.replace(f"{name}.", "")
                            .split("==")[1]
                            for i in self.conf_block(i, conf)
                        }
                        config_dict.update({name: x})
        except Exception as e:
            print(f"[ERROR] [EXCEPTION] {e}")
            return None
        else:
            return config_dict

    def write_conf(self, change: dict):
        conf = self.read_conf()
        setting = self.setting_to_str(change)
        val = list(change.keys())[0]
        if (
            (val in [i[0] for i in conf.items()])
            and (
                list(change.get(val).items())[0][0]
                in [i[0] for i in list(conf.get(val).items())]
            )
            or val in conf.keys()
        ):
            # ? If updating an existing setting or creating a new setting on existing category
            change_list = list(change.get(val).items())[0]
            changed_conf = conf.get(val)
            changed_conf.update({change_list[0]: change_list[1]})
            conf.update({val: changed_conf})
            txt = self.conf_to_str(conf)
            print(txt)
        elif val not in conf.keys():
            # ? If creating a new category
            conf.update(change)
            txt = self.conf_to_str(conf)
        else:
            print("Could not resolve this write")
            txt = None
        with open(CONFIG_FILE, "w") as config:
            for line in txt:
                config.write(line)

    def first_run(self):
        conf = self.read_conf()
        self.write_conf({"run": {"first": "false"}})
        os.system("cls")
        print("Enter your mc folder or nothing for default")
        mc_dir = input("Minecraft Folder: ")
        while (
            (not os.path.exists(mc_dir))
            or (not os.path.exists(f"{mc_dir}/mods"))
            or (not os.path.exists(f"{mc_dir}/versions"))
        ) and mc_dir:
            if not os.path.exists(mc_dir):
                print("[Invalid] The path doesn't exist")
            else:
                print("[Invalid] The given folder is not a mc folder")
            mc_dir = input("Please enter your mc folder: ")
        if mc_dir:
            self.write_conf({"minecraft": {"folder": mc_dir}})
        else:
            self.write_conf({"minecraft": {"folder": DMF}})
        print(f"The config file is found at {CONFIG_FILE}. Change is based on the docx")

    def conf_to_str(self, conf: dict) -> list:
        txt_list = []
        for key, value in conf.items():
            txt_list.append(f"[{key}]\n")
            if isinstance(value, dict):
                for i, j in value.items():
                    txt_list.append(f"\t{key}.{i}=={j}\n")
        return txt_list

    def setting_to_str(self, setting: dict) -> str:
        for key, value in setting.items():
            for i, j in value.items():
                return f"{i}=={f'{key}.{j}' if j.find(key) != -1 else j}"

    def reset_conf(self):
        with open(CONFIG_FILE, "w") as config:
            for line in DC:
                config.write(line)
