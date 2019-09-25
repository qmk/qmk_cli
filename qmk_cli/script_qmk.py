#!/usr/bin/env python3
"""CLI wrapper for running QMK commands.

This program can be run from anywhere, with or without a qmk_firmware repository. If a qmk_firmware repository can be located we will use that to augment our available subcommands.

FIXME(skullydazed/anyone): --help shows underscores where we want dashes in subcommands (EG json_keymap instead of json-keymap)
TODO(skullydazed/anyone): Need a way to filter some subcommands from --help (EG `qmk hello`)
"""
import argparse
import os
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import milc

milc.EMOJI_LOGLEVELS['INFO'] = '{fg_blue}Ψ{style_reset_all}'


@milc.cli.entrypoint('CLI wrapper for running QMK commands.')
def qmk_main(cli):
    """The function that gets run when there's no subcommand.
    """
    cli.print_help()


@lru_cache(maxsize=2)
def in_qmk_firmware():
    """Returns the path to the qmk_firmware we are currently in, or None if we are not inside qmk_firmware.
    """
    cur_dir = Path.cwd()
    while len(cur_dir.parents) > 0:
        found_bin = cur_dir / 'bin' / 'qmk'
        if found_bin.is_file():
            command = [found_bin, '--version']
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode == 0:
                return cur_dir

        # Move up a directory before the next iteration
        cur_dir = cur_dir / '..'
        cur_dir = cur_dir.resolve()


def find_qmk_firmware():
    """Look for qmk_firmware in the usual places.

    This function returns the path to qmk_firmware, or the default location if one does not exist.

    FIXME(skullydazed): add config file support
    """
    if in_qmk_firmware():
        return in_qmk_firmware()

    if 'QMK_HOME' in os.environ:
        return Path(os.environ['QMK_HOME'])

    return Path.home() / 'qmk_firmware'


def main():
    """Setup the environment before dispatching to the entrypoint.
    """
    # Environment setup
    qmk_firmware = find_qmk_firmware()
    os.environ['QMK_HOME'] = str(qmk_firmware)
    os.environ['ORIG_CWD'] = os.getcwd()

    # Import the subcommand modules
    import qmk_cli.subcommands

    if qmk_firmware.exists():
        os.chdir(str(qmk_firmware))
        sys.path.append(str(qmk_firmware / 'lib' / 'python'))
        import qmk.cli

    # Call the entrypoint
    milc.cli()
