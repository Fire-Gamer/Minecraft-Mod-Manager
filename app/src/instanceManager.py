from public.constants import DIF, INSTANCES_FOLDER, INDEX, CURRENT
from public.utils import get_mc_folder, str_to_bool, is_def
import os
import shutil


class InstanceManager(object):
    def __init__(self, instances_names: list):
        self.MF = get_mc_folder()
        self.MODS = f"{self.MF}\\mods"
        self.instances_names = instances_names
        self.current = self.get_current(check=False)

    def __len__(self):
        return len(self.instances_names)

    def create_instance(
        self,
        name: str,
        setting: bool,
        version: str,
        loader: str,
        mods: dict = {},
        check: bool = True,
        ask_open: bool = True,
    ) -> None:
        """Creates a new instance
        Args:
                name (str): name of the instance
                mods (dict): a mod and its path {mod_file_name: path}
                setting (bool): whether is saving the settings or not
                version (str): mc version number
                loader (str): either fabric, forge or vanilla
        Returns:
                None
        """

        if check:
            if name in self.instances_names:
                raise Exception(f"An instance with the name of {name} exists.")
            if os.path.exists(f"{INSTANCES_FOLDER}/{name}.instance"):
                raise Exception(f"An instance with the name of {name} already exists")
            if os.path.isdir(f"{INSTANCES_FOLDER}/{name}.instance"):
                raise Exception(f"A folder with the name of {name} already exists")
        if is_def(name):
            raise Exception(f"The name {name.lower()} is not allowed")
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
        if not (os.path.exists(f"{DIF}\{name}") and os.path.isdir(f"{DIF}\{name}")):
            os.makedirs(f"{DIF}\{name}")
            os.makedirs(f"{DIF}\{name}\mods")
        if setting == True:
            shutil.copy(f"{self.MF}\options.txt", f"{DIF}\{name}\\")
        if ask_open:
            open_folder = input(
                f"Do you want to open the mods folder of {name}([Y], N): "
            )
            if open_folder.lower() == "n":
                return None
            os.system(f'explorer "{DIF}\{name}"')

    def update_index(self) -> None:
        """Updates the index based on the files that exists"""
        with open(f"{INDEX}", "w") as index:
            instances = []
            for file in os.listdir(f"{INSTANCES_FOLDER}"):
                if os.path.isfile(f"{INSTANCES_FOLDER}/{file}"):
                    instances.append(file.lower().strip())
            for name in instances:
                index.write(f"{name[:-9]}\n")

    def read_instance(self, name: str) -> dict:
        """Reads the instance by the given name

        Args:
            name (str): the name of the instance

        Returns:
            dict: the instance's details
        """
        name = name.lower()
        instance_dict = {}
        temp = []
        mods = {}
        with open(f"{INSTANCES_FOLDER}/{name}.instance", "r") as instance:
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
        instance_dict.update({"setting": str_to_bool(temp[-3].split("==")[1].lower())})
        instance_dict.update({"version": temp[-2].split("==")[1]})
        instance_dict.update({"loader": temp[-1].split("==")[1]})
        return instance_dict

    def change_mod_state(self, state: str, mod: str, inst: str = None) -> None:
        """Changes a mod to be disabled or enabled

        Args:
            state (str): enabled or disabled
            mod (str): the mod to change the state
            inst (str, optional): the instance witch contains the mod . Defaults to None.

        Raises:
            Exception: when not a valid state
        """
        inst = self.get_current() if not inst else inst
        if state.lower() not in ["enabled", "disabled"]:
            raise Exception("Not a valid state")
        instance = self.read_instance(inst)
        mods = instance.get("mods")
        mods.update({mod: state.lower()})
        self.create_instance(
            inst,
            instance.get("setting"),
            instance.get("version"),
            instance.get("loader"),
            mods=mods,
            check=False,
        )

    def update_instance(self, name: str) -> None:
        """Update an instance with added mods

        Args:
            name (str): name
        """
        name = name.lower()
        if is_def(name):
            pass
        mods = {}
        inst = self.read_instance(name)
        for i in os.listdir(f"{DIF}\{name}\mods"):
            mods.update({f"{i}": f"true"})
        self.create_instance(
            name,
            inst.get("setting"),
            inst.get("version"),
            inst.get("loader"),
            mods=mods,
            check=False,
            ask_open=False,
        )

    def print_instances(self, instances: list, details: dict) -> None:
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
            print(f"{e}")

    def apply_instance(self, name: str) -> None:
        """Applies an instance with the given name

        Args:
            name (str): name
        """
        name = name.lower()
        if name == "none":
            self.apply_instance("Default")
        else:
            instance = self.read_instance(name)
            for mod in os.listdir(self.MODS):
                os.remove(f"{self.MODS}\\{mod}")
            for mod, enabled in instance.get("mods").items():
                if enabled.lower() == "true":
                    shutil.copy(f"{DIF}\\{name}\\mods\\{mod}", self.MODS)
                else:
                    print(f"Mod {mod} is not enabled")
            #! Removed code ! May not work ! Dangerous
            with open(CURRENT, "w") as cur:
                cur.write(name)
                self.current = name
            if instance.get("setting"):
                shutil.copy(f"{DIF}\\{name}\\options.txt", f"{self.MF}\\options.txt")

    def delete_instance(self, name: str) -> None:
        """Deletes an instance

        Args:
            name (str): name

        Raises:
            Exception: if an instance does not exist

        """
        name = name.lower()
        ins_file = self.get_instance_file(name)
        if name == "default" or name == "none":
            raise Exception("Can't delete default")
        if name not in self.get_instances_names():
            raise Exception(f"An instance with the name {name} doesn't exist")
        confirm = input(
            f"Are you sure you want to delete the instance {name}([Y], N): "
        )
        if confirm.lower() == "n":
            return
        shutil.rmtree(self.get_instance_folder(name))
        os.remove(ins_file)
        self.update_index()
        return

    def get_instances_names(self):
        return [name.lower() for name in self.instances_names]

    def get_instance_folder(self, name) -> str:
        if os.path.exists(folder := f"{DIF}\\{name}") and os.path.isdir(folder):
            return folder
        raise Exception(f"An instance named {name} doesn't exists.")

    def get_current(self, check: bool = True) -> str:
        with open(CURRENT, "r") as cur:
            current = cur.readline()
            if check:
                if not current:
                    raise Exception("No current instance selected")
        return current if current else None

    def get_instance_file(self, name: str):
        name = name.lower()
        with open(f"{INDEX}", "r") as index:
            instance_names = []
            for instance in index.readlines():
                instance_names.append(instance.strip())
            for instance in instance_names:
                if instance.lower() == name.lower() and os.path.exists(
                    f"{INSTANCES_FOLDER}\{name.lower()}.instance"
                ):
                    return f"{INSTANCES_FOLDER}\{name.lower()}.instance"
            raise Exception(f"An instance with the name '{name}' does not exist")
