import importlib
import inspect
import logging
import os
import subprocess
from _importlib_modulespec import Loader
from importlib import util
from types import ModuleType
from typing import Optional

import click

from pado.directory_traversal import get_all_pados_in_directory
from pado.runbook import print_markdown, Runbook
from pado.runbook_template import create_new_runbook


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
@click.option('--raw', is_flag=True, default=False,
              help='Run the pado file with "python FILENAME" in the shell instead of as a class')
def run(filename, retry, raw):
    """
    run a print-and-do file
    """
    if raw:
        subprocess.call(['python', filename])
    else:
        run_print_and_do_file_by_instantiating_class(filename)


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
