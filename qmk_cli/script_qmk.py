#!/usr/bin/env python3
"""CLI wrapper for running QMK commands.

This program can be run from anywhere, with or without a qmk_firmware checkout. It provides a small set of subcommands for working with QMK and otherwise dispatches to the `qmk_firmware/bin/qmk` script for the repo you are currently in, or your default repo if you are not currently in a qmk_firmware checkout.

FIXME(skullydazed): --help shows underscores where we want dashes in subcommands (EG json_keymap instead of json-keymap)
"""
import argparse
import os
import subprocess
import sys
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from pkgutil import walk_packages

import milc


SUBCOMMAND_BLACKLIST = ['qmk.cli.subcommands']
milc.EMOJI_LOGLEVELS['INFO'] = '{fg_blue}Ψ{style_reset_all}'


@milc.cli.entrypoint('CLI wrapper for running QMK commands.')
def qmk_main(cli):
    """The function that gets run when there's no subcommand.
    """
    cli.print_help()


def subcommand_modules():
    """Returns a list of subcommands
    """
    for pkg in walk_packages():
        if 'qmk_cli.subcommands.' in pkg.name or 'qmk.cli.' in pkg.name:
            yield pkg.name


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
    """Dispatch the CLI subcommand to the proper place.

    We first check to see if the subcommand was provided by the global `qmk`. If it was we import that module and hand control over to the entrypoint.

    All other subcommands are dispatched to the local `qmk`, either the one we are currently in or whatever the user's default qmk_firmware is.
    """
    # Environment setup
    qmk_firmware = find_qmk_firmware()
    os.environ['QMK_HOME'] = str(qmk_firmware)
    qmk_bin = qmk_firmware / 'bin' / 'qmk'
    qmk_lib = qmk_firmware / 'lib' / 'python'
    sys.path.append(str(qmk_lib))

    subcommand = None

    for count, arg in enumerate(sys.argv[1:]):
        if arg and arg[0] != '-':
            sys.argv[count+1] = subcommand = arg.replace('-', '_')
            subcommand = subcommand.replace('_', '.')
            break

    if not subcommand:
        # Import all the subcommand modules so --help works correctly
        for subcommand_module in subcommand_modules():
            if subcommand_module in SUBCOMMAND_BLACKLIST:
                continue

            try:
                import_module(subcommand_module)

            except ModuleNotFoundError as e:
                if e.name != subcommand_module:
                    raise

    else:
        subcommand_module = None

        for module in subcommand_modules():
            if subcommand in module:
                subcommand_module = module
                break  # First match wins

        if subcommand_module:
            if subcommand_module.startswith('qmk.cli.'):
                os.environ['ORIG_CWD'] = os.getcwd()
                os.chdir(str(qmk_firmware))

            import_module(subcommand_module)

        else:
            print("Ψ Can't find subcommand %s!" % (subcommand,))  # milc.cli.log is not available at this point in execution
            exit(255)

    # Call the entrypoint
    milc.cli()
