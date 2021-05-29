import importlib.util
import inspect
import logging
import os

from pado.runbook import Runbook


def get_all_pados_in_directory(directory, recursively=False):
    """
    :returns List of all Print-And-Do files in directory

    Print-And-Do files are defined as a .py file containing a class that extends Runbook
    """

    names = []
    if not directory:
        logging.info("No directory provided, using .")
        directory = "."
    # traverse current_directory directory, and list directories as directories_in_cd and files as files_in_cd
    # This currently imports all modules, which results in running code. This is very problematic for files such as
    # setup.py and others without __name__=="__main__" blocks. Use with caution
    for current_directory, directories_in_cd, files_in_cd in os.walk(directory):
        path = current_directory.split(os.sep)
        logging.info("\tTraversing " + current_directory)
        if '.' in path:
            path.remove('.')
        if any(x.startswith('.') or x.startswith('_') for x in path):
            continue
        # excluded_folders = ['__pycache__', 'build', 'temp', 'pado-venv']
        # if all(x not in current_directory for x in excluded_folders) and not os.path.basename(
        #        current_directory).startswith('.'):
        for name in get_modules_in_package(current_directory):
            logging.info("Adding " + name)
            names.append(name)
        if not recursively:
            break
        # logging.info(current_directory)
        # logging.info((len(path) - 1) * '---', os.path.basename(current_directory))
        # for dir in directories_in_cd:
        #    logging.info(len(path) * '--|', dir)
        # for file in files_in_cd:
        #    logging.info(len(path) * '---', file)
    logging.info(f"Full list of PADos found: {names}")
    return names
    # for name, cls in inspect.getmembers(sys.modules['example.my-first-pad'], inspect.isclass):
    #    if cls.__module__ == "pado.runbook":
    #        pass
    #    else:
    #        logging.info(cls)
    # logging.info(sys.modules['example.my-first-pad'])


def get_modules_in_package(package_name: str):
    if package_name:
        files = os.listdir(package_name)
    else:
        files = os.listdir()
    for file in files:
        if not file.startswith("_") and file not in ["setup.py", ]:
            if file[-3:] != '.py':
                continue

            file_name = file[:-3]
            module_name = package_name + '.' + file_name if package_name != "" else file_name
            logging.debug("Module name: " + module_name)
            logging.debug("abspath: " + os.path.abspath(file))
            file_path = os.path.abspath(package_name + "/" + file if package_name != "" else file)

            if (spec := importlib.util.spec_from_file_location(file_name, file_path)) is not None:
                # If you chose to perform the actual import ...
                module = importlib.util.module_from_spec(spec)
                logging.info(f"{module_name!r} has been imported")
                spec.loader.exec_module(module)
                classes = [cls for _, cls in
                           inspect.getmembers(module, inspect.isclass)]
                logging.info(f"Found classes: {classes} in file: {file}")
                if Runbook in classes:
                    yield module_name
            else:
                logging.info(f"can't find the {module_name!r} module")

                # logging.info(file_name + " is a PADo")
            # for name, cls in inspect.getmembers(sys.modules[module_name], inspect.isclass):
            # logging.info("name: " + name)
            # logging.info("cls.__module__: " + cls.__module__)
            #    if cls.__module__ == "pado.runbook":
            #        yield name, cls
