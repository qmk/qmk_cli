#!/usr/bin/env python3
"""CLI wrapper for running QMK commands.

This program can be run from anywhere, with or without a qmk_firmware checkout. It provides a small set of subcommands for working with QMK and otherwise dispatches to the `qmk_firmware/bin/qmk` script for the repo you are currently in, or your default repo if you are not currently in a qmk_firmware checkout.
"""
import argparse
import os
import subprocess
import sys
from functools import lru_cache
from importlib import import_module
from pathlib import Path


@lru_cache(maxsize=2)
def in_qmk_firmware():
    """Returns the path to the qmk_firmware we are currently in, or None if we are not inside qmk_firmware.
    """
    cur_dir = Path.cwd()
    while len(cur_dir.parents) > 0:
        found_bin = cur_dir / 'bin' / 'qmk'
        if found_bin.is_file():
            command = [found_bin, '--version']
            result = subprocess.run(command)

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


def parse_args():
    """Process arguments outside milc.
    """
    parser = argparse.ArgumentParser(description='CLI wrapper for running QMK commands.')
    parser.add_argument('-H', '--home', help='Path to the qmk_firmware directory.')
    parser.add_argument('subcommand', help='Subcommand to run')
    parser.add_argument('subcommand_args', nargs=argparse.REMAINDER, help='Arguments to pass to the subcommand.')
    args = parser.parse_args()

    if args.home:
        os.environ['QMK_HOME'] = args.home

    return (args.subcommand, args.subcommand_args)


def main():
    """Dispatch the CLI subcommand to the proper place.

    We first check to see if the subcommand was provided by the global `qmk`. If it was we import that module and hand control over to the entrypoint.

    All other subcommands are dispatched to the local `qmk`, either the one we are currently in or whatever the user's default qmk_firmware is.
    """
    subcommand, subcommand_args = parse_args()
    subcommand_module = 'qmk_cli.subcommands.' + subcommand
    sys.argv = ['qmk-'+subcommand] + subcommand_args
    qmk_firmware = find_qmk_firmware()
    qmk_bin = qmk_firmware / 'bin' / 'qmk'
    os.environ['QMK_HOME'] = str(qmk_firmware)

    try:
        # Attempt to import the subcommand from qmk_cli first
        import qmk_cli.milc
        import_module(subcommand_module)
        qmk_cli.milc.cli()

    except ImportError as e:
        # Check to make sure there's not a bad import statement in qmk_cli
        if e.name != subcommand_module:
            raise

        # Dispatch to the underlying `qmk_firmware/bin/qmk`
        if qmk_bin.is_file() and os.access(str(qmk_bin), os.X_OK):
            argv = ['python3', str(qmk_bin), subcommand] + subcommand_args
            os.execvp('python3', argv)

        # Tell the user we can't continue
        print('*** Could not locate qmk_firmware directory!')
        exit(255)


if __name__ == '__main__':
    main()
