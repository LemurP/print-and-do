import logging
import subprocess

import click

from pado.directory_traversal import get_all_pados_in_directory
from pado.runbook import print_markdown
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
@click.argument('filename', type=click.STRING)
def show(filename):
    """
    render the contents of a log file in the terminal
    """
    with open(filename) as file_:
        text = file_.read()
    print_markdown(text)


@main.command()
@click.argument('filename', type=click.STRING)
# @click.option('--retry', is_flag=True, default=False, help='Retry a pado from start.')
def run(filename):
    """
    run a print-and-do file
    """
    subprocess.call(['python', filename])


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
