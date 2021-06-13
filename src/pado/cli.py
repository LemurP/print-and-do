import importlib
import inspect
import json
import logging
import os
import subprocess
from importlib import util
from importlib.abc import Loader
from pathlib import Path
from types import ModuleType
from typing import Optional, List

import appdirs
import click

from pado.directory_traversal import get_all_pados_in_directory
from pado.runbook import print_markdown, Runbook
from pado.runbook_template import create_new_runbook

# Constants TODO: Should be stored in a specific file
REGISTERED_PADOS_JSON_FIELD = 'registered_pados'
CONFIG_FILENAME = 'config.json'
pado_config_name = 'pado'


@click.group('pado')
@click.option('--log', type=click.Choice(["DEBUG", "INFO", "WARNING"], case_sensitive=False), default="WARNING")
def main(log):
    logging.getLogger().setLevel(log)
    pass


@main.command(short_help="create a new print-and-do file")
@click.argument('title', type=click.STRING)
def new(title):
    """
    create a new print-and-do file named TITLE
    """

    filename = create_new_runbook(title)
    print(f"\ncreated new pado '{filename}'\n")


@main.command()
@click.argument('filename', type=click.Path(exists=True))
def show(filename):
    """
    render the contents of a log file in the terminal
    """
    with open(filename) as file_:
        text = file_.read()
    print_markdown(text)


@main.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--retry', is_flag=True, default=False, help='Retry a pado from start.')
@click.option('--noregister', is_flag=True, default=False, help='Don\'t register in the list of known pados.')
@click.option('--raw', is_flag=True, default=False,
              help='Run the pado file with "python FILENAME" in the shell instead of as a class')
def run(filename, retry, raw, noregister):
    """
    run a print-and-do file
    """
    if raw:
        subprocess.call(['python', filename])
    else:
        run_print_and_do_file_by_instantiating_class(filename)
    # if not noregister:
    #     register_pado_in_list_of_known_pados


def run_print_and_do_file_by_instantiating_class(filename):
    file_path = os.path.abspath(filename)
    logging.debug(
        f"filename={filename}, file_path={file_path}. imported ModuleSpec = {importlib.util.spec_from_file_location(filename, file_path)}")
    if (spec := importlib.util.spec_from_file_location(filename, file_path)) is not None:
        # If you chose to perform the actual import ...
        module: ModuleType = importlib.util.module_from_spec(spec)
        logging.info(f"{module!r} has been imported")
        loader: Optional[Loader] = spec.loader
        loader.exec_module(module)
        classes = [cls for _, cls in
                   inspect.getmembers(module, inspect.isclass)]
        logging.info(f"Found classes: {classes} in file: {filename}")
        if Runbook in classes:
            classes[0](f"{classes[0]._make_pretty_name(classes[0].__name__).lower()}.log").run()
    else:
        logging.info(f"can't find the {filename!r} module")


@main.command(short_help="register print-and-do file")
@click.argument('filename', type=click.Path(exists=True))
def register(filename):
    """
    register the print-and-do file in pados central configuration.
    This will then be shown when running `pado list`
    """

    CONFIG_DIR = Path(appdirs.user_config_dir(appname=pado_config_name))  # magic
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = CONFIG_DIR / CONFIG_FILENAME
    if not config.exists():
        logging.debug(f"Config file does not exist: {config}")
        data = {REGISTERED_PADOS_JSON_FIELD: [str(Path(filename).absolute())]}
        with config.open('w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    with config.open('r') as f:
        logging.debug(f"Config file exists: {config}")
        configuration = json.load(f)  # now 'configuration' can safely be imported from this module
        logging.debug(f"config file contains: {configuration}")


@main.command(short_help="list print-and-do files")
@click.argument('directory', type=click.STRING, default="")
@click.option('--certain', is_flag=True,
              prompt='This is in BETA, it will load all modules in the given directory to check. Are you certain you want to do that?')
# @click.option('--retry', is_flag=True, default=False, help='Retry a pado from start.')
def list(directory, certain):
    """
    list print-and-do files in DIRECTORY
    """
    if certain:
        for pado in get_all_pados_in_directory(directory):
            print(pado)


def read_known_pados_from_config() -> List[str]:
    CONFIG_DIR = Path(appdirs.user_config_dir(appname=pado_config_name))  # magic
    if not CONFIG_DIR.exists():
        logging.debug(f"No config folder found: {CONFIG_DIR} does not exist")
        return []

    config = CONFIG_DIR / CONFIG_FILENAME
    if not config.exists():
        logging.debug(f"Config file does not exist: {config}")
        return []
    with config.open('r') as f:
        logging.debug(f"Config file exists: {config}")
        configuration = json.load(f)  # now 'configuration' can safely be imported from this module
        logging.debug(f"config file contains: {configuration}")
        known_pados = configuration[REGISTERED_PADOS_JSON_FIELD]
        return known_pados


def pretty_print_known_pados(known_pados):
    print("Known pados:")
    for pado in known_pados:
        print(f"\t{pado}")


@main.command(short_help="list known print-and-do files")
def listknown():
    """
    list known print-and-do files
    """
    known_pados = read_known_pados_from_config()
    pretty_print_known_pados(known_pados)
