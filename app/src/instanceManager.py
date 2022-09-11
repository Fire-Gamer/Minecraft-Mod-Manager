from public.constants import *
import os
import shutil


class InstanceManager(object):
    def __init__(self, instances_names: list):
        self.instances_names = instances_names

    def create_instance(
        self,
        name: str,
        setting: bool,
        version: str,
        loader: str,
        mods: dict = {},
        check: bool = True,
    ) -> None:
        """Creates a new instance
        Args:
                name (str): name of the instance
                mods (dict): a mod and its path {mod_file_name: path}
                setting (bool): path of the setting file
                version (str): mc version number
                loader (str): either fabric or forge
        Returns:
                None
        """

        if name in self.instances_names:
            print(f"[ERROR] [Invalid] An instance with the name of {name} exists.")
            return None
        else:
            instance = {
                "name": name.capitalize(),
                "mods": mods,
                "setting": setting,
                "version": version,
                "loader": loader,
            }

        self.instances_names += instance.get("name")
        if instance is None:
            return
        if check:
            if os.path.exists(f"{INSTANCES_FOLDER}/{name}.instance"):
                print(
                    f"[ERROR] [INFO] An instance with the name of {name} already exists"
                )
                return None
            if os.path.isdir(f"{INSTANCES_FOLDER}/{name}.instance"):
                print(f"[ERROR] [INFO] A folder with the name of {name} already exists")
                return None
        save: str
        save = f"name=={instance.get('name')}\n[\n\t\u007b\n"
        for mod, enabled in instance.get("mods").items():
            save += f"\t\t{mod}: '{enabled}',\n"
        save += (
            f"\t\u007d,\n\n\t"
            f"save_settings=={str(instance.get('setting')).lower()},\n\t"
            f"version=={instance.get('version')},\n\t"
            f"loader=={instance.get('loader')}\n]"
        )

        with open(f"{INSTANCES_FOLDER}/{name.lower()}.instance", "w") as ins, open(
            f"{INDEX}", "a"
        ) as index:
            ins.write(save)
            index.write(f"{instance.get('name')}\n")
        os.makedirs(f"{DIF}\{name}")
        os.makedirs(f"{DIF}\{name}\mods")
        if setting == True:
            shutil.copy(f"{DMF}\options.txt", f"{DIF}\{name}\\")
        # Todo Make a settings file

    def get_instances_names(self):
        return self.instances_names

    def get_instance_file(self, name: str):
        with open(f"{INDEX}", "r") as index:
            instance_names = []
            for instance in index.readlines():
                instance_names.append(instance.strip())
            for instance in instance_names:
                if instance.lower() == name.lower() and os.path.exists(
                    f"{INSTANCES_FOLDER}/{name.lower()}.instance"
                ):
                    return f"{INSTANCES_FOLDER}/{name.lower()}.instance"
                else:
                    print(f"[ERROR] [Exception] Index file is corrupted please update.")
                    return None
        print(f"[ERROR] [Invalid] An instance with the name '{name}' does not exist")
        return None

    def update_index(self):
        with open(f"{INDEX}", "w") as index:
            instances = []
            for file in os.listdir(f"{INSTANCES_FOLDER}"):
                if os.path.isfile(f"{INSTANCES_FOLDER}/{file}"):
                    instances.append(file.lower().strip())
            for name in instances:
                index.write(f"{name[:-9]}\n")

    def read_instance(self, name: str):
        # TODO Rename temp
        instance_dict = {}
        temp = []
        mods = {}
        with open(f"{INSTANCES_FOLDER}/{name.lower()}.instance", "r") as instance:
            for line in instance.readlines():
                temp.append(line.strip().replace(",", ""))
        for i in ["[", "]", ""]:
            if i in temp:
                temp.remove(i)
        for i in temp[2:-4]:
            mods.update(
                {i.strip().split(":")[0]: i.strip().split()[1].replace("'", "")}
            )
        instance_dict.update({"name": temp[0].split("==")[1].capitalize()})
        instance_dict.update({"mods": mods})
        instance_dict.update(
            {"setting": True if temp[-3].split("==")[1].lower() == "true" else False}
        )
        instance_dict.update({"version": temp[-2].split("==")[1]})
        instance_dict.update({"loader": temp[-1].split("==")[1]})
        return instance_dict

    def update_instance(self, name: str):
        mods = {}
        for i in os.listdir(f"{DIF}\{name}"):
            # TODO change to deactivate and activate instances
            mods.update({f"{i}": f"true"})
        self.create_instance(
            name,
            self.read_instance("setting"),
            self.read_instance("version"),
            self.read_instance("loader"),
            mods=mods,
            check=False,
        )

    def print_instances(self, instances: list, details: dict):
        """Prints the given instances

        Args:
                instances (list): the list of instances
                details (dict): each detail of instances
        """
        try:
            len_max = 0
            for instance in instances:
                if len(instance) > len_max:
                    len_max = len(instance)
            len_max += 10
            print(
                f"\033[4m{'Name':^{len_max}}|{'Version':^16}|{'MC Loader':^16}\033[0m"
            )
            for instance in instances:
                print(
                    f"{instance:^{len_max}}|{details.get(instance).get('version'):^16}|"
                    f"{details.get(instance).get('loader'):^16}"
                )
        except Exception as e:
            print(f"[Error] [Exception] {e}")

    def apply_instance(self, name):
        instance = self.read_instance(name)
        for mod, enabled in instance.get("mods").items():
            if enabled.lower() == "true":
                shutil.copy(f"{DIF}\\{name}\\mods\\{mod}", f"{DMF}\\mods\\")
            else:
                print(f"Mod {mod} is not enabled")


# TODO Simplify every thing
