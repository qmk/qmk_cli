#!/usr/bin/env python3
"""CLI wrapper for running QMK commands.

This program can be run from anywhere, with or without a qmk_firmware repository. If a qmk_firmware repository can be located we will use that to augment our available subcommands.
"""
import os
import shlex
import subprocess
import sys
from platform import platform
from traceback import print_exc

import milc

from . import __version__
from .helpers import find_qmk_firmware, is_qmk_firmware

milc.set_metadata(version=__version__)
milc.EMOJI_LOGLEVELS['INFO'] = '{fg_blue}Ψ{style_reset_all}'

# These must happen after the milc.set_metadata() call
import milc.subcommand.config  # noqa, must come after milc.set_metadata()
from milc.questions import yesno


@milc.cli.entrypoint('CLI wrapper for running QMK commands.')
def qmk_main(cli):
    """The function that gets run when there's no subcommand.
    """
    cli.print_help()


def run_cmd(*command):
    """Run a command in a subshell.
    """
    if 'windows' in milc.cli.platform.lower():
        safecmd = map(shlex.quote, command)
        safecmd = ' '.join(safecmd)
        command = [os.environ['SHELL'], '-c', safecmd]

    return subprocess.run(command)


# Python setuptools entrypoint
def main():
    """Setup the environment before dispatching to the entrypoint.
    """
    # Warn if they use an outdated python version
    if sys.version_info < (3, 7):
        print('Warning: Your Python version is out of date! Some subcommands may not work!')
        print('Please upgrade to Python 3.7 or later.')

    if 'windows' in platform().lower():
        msystem = os.environ.get('MSYSTEM', '')

        if 'mingw64' not in sys.executable or 'MINGW64' not in msystem:
            print('ERROR: It seems you are not using the MINGW64 terminal.')
            print('Please close this terminal and open a new MSYS2 MinGW 64-bit terminal.')
            print('Python: %s, MSYSTEM: %s' % (sys.executable, msystem))
            exit(1)

    # Environment setup
    qmk_firmware = find_qmk_firmware()
    os.environ['QMK_HOME'] = str(qmk_firmware)
    os.environ['ORIG_CWD'] = os.getcwd()

    import qmk_cli.subcommands

    # Check out and initialize the qmk_firmware environment
    if is_qmk_firmware(qmk_firmware):
        # All subcommands are run relative to the qmk_firmware root to make it easier to use the right copy of qmk_firmware.
        os.chdir(str(qmk_firmware))
        sys.path.append(str(qmk_firmware / 'lib/python'))

        try:
            import qmk.cli  # noqa

        except ImportError as e:
            if qmk_firmware.name != 'qmk_firmware':
                print('Warning: %s does not end in "qmk_firmware". Do you need to set QMK_HOME to "%s/qmk_firmware"?' % (qmk_firmware, qmk_firmware))

            print('Error: %s: %s', (e.__class__.__name__, e))
            print_exc()
            sys.exit(1)

    # Call the entrypoint
    return_code = milc.cli()

    if return_code is False:
        exit(1)

    elif return_code is not True and isinstance(return_code, int):
        if return_code < 0 or return_code > 255:
            milc.cli.log.error('Invalid return_code: %d', return_code)
            exit(255)

        exit(return_code)

    exit(0)
