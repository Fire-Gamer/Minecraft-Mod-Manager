from public.constants import (
    MMMF,
    CONFIG_FOLDER,
    INSTANCES_FOLDER,
    DIF,
    CURRENT,
    INDEX,
    DC,
    CONFIG_FILE,
)
from src.instanceManager import InstanceManager
from src.config import Config
import argparse
import os

os.system("")

# TODO better var names and docs


def create_dirs():
    returning = False
    if not (os.path.exists(MMMF)):
        os.makedirs(MMMF)
        returning = True
    if not (os.path.exists(CONFIG_FOLDER)):
        os.makedirs(CONFIG_FOLDER)
        returning = True
    if not (os.path.exists(INSTANCES_FOLDER)):
        os.makedirs(INSTANCES_FOLDER)
        returning = True
    if not (os.path.exists(DIF)):
        os.makedirs(DIF)
        returning = True
    if not (os.path.exists(CURRENT)):
        with open(CURRENT, "w") as cur:
            pass
        returning = True
    if not os.path.exists(INDEX):
        with open(INDEX, "w") as index:
            pass
        returning = True
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as conf:
            for i in DC:
                conf.write(i)
        returning = True
    if returning:
        return True
    else:
        return False


def create(args):
    instanceManager = create_instance_manager()
    instanceManager.create_instance(
        args.name, True if args.settings == "true" else False, args.version, args.loader
    )
    instanceManager.update_index()


def initialize(args):
    if create_dirs():
        Config()
        instanceManager = create_instance_manager()
        instanceManager.create_instance("Default", False, "None", "vanilla")
    else:
        print("Already initialized")


def lst(args):
    instanceManager = create_instance_manager()
    if len(instanceManager.get_instances_names()) == 0:
        raise Exception("No instances created use 'mmm create' to make a new one")
    if not args.simple:
        instanceManager.update_index()
        details = {}
        instances = instanceManager.get_instances_names()
        for instance in instances:
            detail = {
                "loader": instanceManager.read_instance(instance).get("loader"),
                "version": instanceManager.read_instance(instance).get("version"),
            }
            details.update({instance: detail})
        instanceManager.print_instances(instances, details)
        return
    for index, name in enumerate(instanceManager.get_instances_names()):
        print(f"{index+1}{name.capitalize()}")


def apply(args):
    instanceManager = create_instance_manager()
    instanceManager.apply_instance(args.name)
    instanceManager.update_index()


def update(args):
    instanceManager = create_instance_manager()
    instanceManager.update_instance(args.name)
    instanceManager.update_index()


def delete(args):
    instanceManager = create_instance_manager()
    instanceManager.delete_instance(args.name)
    instanceManager.update_index()


def fix_index(args):
    instanceManager = create_instance_manager()
    instanceManager.update_index()


def enable(args):
    instanceManager = create_instance_manager()
    if args.inst and args.inst in instanceManager.get_instances_names():
        instanceManager.change_mod_state("enabled", args.mod, args.inst)
    instanceManager.change_mod_state("enabled", args.mod)
    instanceManager.update_index()


def disable(args):
    instanceManager = create_instance_manager()
    if args.inst and args.inst in instanceManager.get_instances_names():
        instanceManager.change_mod_state("disabled", args.mod, args.inst)
    instanceManager.change_mod_state("disabled", args.mod)
    instanceManager.update_index()


def show_details(args):
    instanceManager = create_instance_manager()
    if not args.name in instanceManager.get_instances_names():
        raise Exception(f"No instance with name of {args.name}")
    print(f"Name: {args.name}")
    print(f"Mods: ")
    instance = instanceManager.read_instance(args.name)
    for mod, state in instance.get("mods"):
        print(f"\t  {mod}: {state}")
    print(f"Save settings: {instance.get('setting')}")
    print(f"Version: {instance.get('version')}")
    print(f"Loader: {instance.get('loader')}")


def args():
    # Main parser (Parent)
    parser = argparse.ArgumentParser(
        description="Manage your minecraft mods using this CLI",
        usage="%(prog)s [options]",
    )
    subparser = parser.add_subparsers(dest="cmd")
    # Making subparser required
    subparser.required = True

    init_parser = subparser.add_parser("init", help="Initialize mmm")
    init_parser.set_defaults(func=initialize)

    # Create parser
    create_parser = subparser.add_parser(
        "create", help="Creates a new instance with specified arguments"
    )
    create_parser.add_argument(
        "name", type=str, help="name of instance that is going to be created"
    )
    create_parser.add_argument(
        "settings",
        choices=["true", "false"],
        help="weather to save settings file or not",
    )
    create_parser.add_argument("version", type=str, help="MC version to be saved")
    create_parser.add_argument(
        "loader", choices=["fabric", "forge", "vanilla"], help="Loader type"
    )
    create_parser.set_defaults(func=create)

    # List parser
    lst_parser = subparser.add_parser("list", help="Lists all the available instances")
    lst_parser.add_argument("-s", "--simple", action="store_true", dest="simple")
    lst_parser.set_defaults(func=lst)

    # Apply parser
    apply_parser = subparser.add_parser(
        "apply", help="Applies the specified instance to mods folder"
    )
    apply_parser.add_argument("name", help="name of an instance")
    apply_parser.set_defaults(func=apply)

    # Update parser
    update_parser = subparser.add_parser(
        "update", help="Update an instance after adding mods"
    )
    update_parser.add_argument(
        "name", type=str, help="The name of the instance to be updated"
    )
    update_parser.add_argument("-s", "--setting", action="store_true")
    update_parser.set_defaults(func=update)

    # Delete parser
    delete_parser = subparser.add_parser(
        "delete", help="Delete an instance with the specified name"
    )
    delete_parser.add_argument("name", help="Name of instance to delete")
    delete_parser.set_defaults(func=delete)

    index_parser = subparser.add_parser("index", help="Fixes the index if corrupted")
    index_parser.set_defaults(func=fix_index)

    disable_parser = subparser.add_parser(
        "disable", help="disable a mode in the current instance or a specified instance"
    )
    disable_parser.add_argument("mod", help="The mod to disable")
    disable_parser.add_argument(
        "-i", "--instance", help="An instance in which the mod is found", dest="inst"
    )
    disable_parser.set_defaults(func=disable)

    enable_parser = subparser.add_parser(
        "enable", help="disable a mode in the current instance or a specified instance"
    )
    enable_parser.add_argument("mod", help="The mod to to enable")
    enable_parser.add_argument(
        "-i", "--instance", help="An instance in which the mod is found", dest="inst"
    )
    enable_parser.set_defaults(func=enable)

    details_parser = subparser.add_parser(
        "details", help="Show the details of instance with a given name"
    )
    details_parser.add_argument("name", help="The name of the instance")
    details_parser.set_defaults(func=show_details)

    # ? Parsing args and redirecting to the respective function
    args = parser.parse_args()
    args.func(args)


def create_instance_manager():
    instances = []
    with open(INDEX, "r") as index:
        for instance in index.readlines():
            instances.append(instance.strip())
    instanceManager = InstanceManager(instances)
    return instanceManager


def main():
    try:
        args()
    except Exception as e:
        print(f"[EXCEPTION] [ERROR] {e}")
    finally:
        pass


if __name__ == "__main__":
    main()
