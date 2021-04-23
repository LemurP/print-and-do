import subprocess

import click

from pado.runbook import print_markdown
from pado.runbook_template import create_new_runbook


@click.group('pado')
def main():
    """
    runbook-py module command line helper
    """
    pass


@main.command()
@click.argument('title', type=click.STRING)
def new(title):
    """
    create a new runbook file named TITLE
    """

    filename = create_new_runbook(title)
    print(f"\ncreated new runbook '{filename}'\n")


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
def run(filename):
    """
    run a print-and-do file
    """
    subprocess.call(['python', filename])
