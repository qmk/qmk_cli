"""Prints environment information.
"""
import os

from milc import cli


@cli.argument('var', default=None, nargs='?', help='Optional variable to query')
@cli.subcommand('Prints environment information.')
def env(cli):
    data = {
        'QMK_HOME' : os.environ.get('QMK_HOME', "")
    }

    if cli.args.var:
        # dump out requested arg
        print(data[cli.args.var])
    else:
        # dump out everything
        for key,val in data.items():
            print(f'{key}="{val}"')
