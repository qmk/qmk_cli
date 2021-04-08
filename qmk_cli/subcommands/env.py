"""Prints environment information.
"""
import os
from pathlib import Path

from milc import cli
from qmk_cli.helpers import is_qmk_firmware


@cli.argument('var', default=None, nargs='?', help='Optional variable to query')
@cli.subcommand('Prints environment information.')
def env(cli):
    home = os.environ.get('QMK_HOME', "")
    data = {
        'QMK_HOME': home,
        'QMK_FIRMWARE': home if is_qmk_firmware(Path(home)) else ""
    }

    # Now munge the current cli config
    for key, val in cli.config.general.items():
        converted_key = 'QMK_' + key.upper()
        data[converted_key] = val

    if cli.args.var:
        # dump out requested arg
        print(data[cli.args.var])
    else:
        # dump out everything
        for key, val in data.items():
            print(f'{key}="{val}"')
