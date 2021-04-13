import click

from unquietcode.tools.runbook import create_new_runbook
from unquietcode.tools.runbook.runbook import print_markdown


@click.group('python3 -m runbook')
def entrypoint():
    """
    runbook-py module command line helper
    """
    pass


@entrypoint.command()
@click.argument('title', metavar='title', type=click.STRING, required=True)
def new(title):
    """
    create a new runbook file
    """

    filename = create_new_runbook(title)
    print(f"\ncreated new runbook '{filename}'\n")


@entrypoint.command()
@click.argument('filename', metavar='filename', type=click.STRING, required=True)
def show(filename):
    """
    render the contents of a log file in the terminal
    """
    with open(filename) as file_:
        text = file_.read()
    print_markdown(text)


# module entrypoint
entrypoint(prog_name='python3 -m runbook')
