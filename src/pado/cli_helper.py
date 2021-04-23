import signal
import sys

import click


@click.command()
@click.option('--retry', default=False, help='Retry a pado from start.')
@click.argument('filename', type=click.STRING, required=False)
@click.pass_context
def main(ctx, retry, filename):
    # setup a signal handler for better output on CTRL-C
    def signal_handler(sig, frame):
        print('\n')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    return filename, retry
