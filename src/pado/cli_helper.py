import signal
import sys

import click


@click.command()
@click.argument('filename', type=click.STRING, required=False)
def main(filename):
    # setup a signal handler for better output on CTRL-C
    def signal_handler(sig, frame):
        print('\n')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    return filename
