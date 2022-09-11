from public.constants import *
from src.instanceManager import InstanceManager
from src.config import Config
import argparse
import os

os.system("")

# TODO better var names and docs


def create_dirs():
    if not (os.path.exists(MMMF)):
        os.makedirs(MMMF)
    if not (os.path.exists(CONFIG_FOLDER)):
        os.makedirs(CONFIG_FOLDER)
    if not (os.path.exists(INSTANCES_FOLDER)):
        os.makedirs(INSTANCES_FOLDER)
    if not (os.path.exists(DIF)):
        os.makedirs(DIF)
    if not os.path.exists(INDEX):
        with open(INDEX, "w") as index:
            pass
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as conf:
            for i in DC:
                conf.write(i)


def create(args):
    instanceManager = create_instance_manager()
    instanceManager.create_instance(
        args.name, True if args.settings == "true" else False, args.version, args.loader
    )


def lst(args):
    arg = args
    instanceManager = create_instance_manager()
    details = {}
    instances = instanceManager.get_instances_names()
    for instance in instances:
        detail = {
            "loader": instanceManager.read_instance(instance).get("loader"),
            "version": instanceManager.read_instance(instance).get("version"),
        }
        details.update({instance: detail})
    instanceManager.print_instances(instances, details)


def apply(args):
    instanceManager = create_instance_manager()
    instanceManager.apply_instance(args.name)


def update(args):
    pass


def args():
    # Main parser (Parent)
    parser = argparse.ArgumentParser(
        description="Manage your minecraft mods using this CLI",
        usage="%(prog)s [options]",
    )
    subparser = parser.add_subparsers(dest="cmd")
    # Making subparser required
    subparser.required = True

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
        create_dirs()
        config = Config()
        args()
    except Exception as e:
        print(f"[EXCEPTION] [ERROR] {e}")
    finally:
        pass


if __name__ == "__main__":
    main()
