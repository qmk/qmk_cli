"""Useful helper functions.
"""
import os
from functools import lru_cache
from importlib.util import find_spec
from pathlib import Path

from milc import cli


def is_qmk_firmware(qmk_firmware):
    """Returns True if the given Path() is a qmk_firmware clone.
    """
    paths = [
        qmk_firmware,
        qmk_firmware / 'quantum',
        qmk_firmware / 'requirements.txt',
        qmk_firmware / 'requirements-dev.txt',
        qmk_firmware / 'lib/python/qmk/cli/doctor.py'
    ]

    for path in paths:
        if not path.exists():
            return False

    return True


def broken_module_imports():
    """Make sure we can import all the python modules.
    """
    broken_modules = find_broken_requirements('requirements.txt')
    broken_dev_modules = find_broken_requirements('requirements-dev.txt') if cli.config.user.developer else []
    to_return = [False, False]

    if broken_modules:
        to_return[0] = True

    if broken_dev_modules:
        to_return[1] = True

    for module in broken_modules + broken_dev_modules:
        print('Could not find module %s!' % module)

    return to_return


def find_broken_requirements(requirements):
    """ Check if the modules in the given requirements.txt are available.

    Args:

        requirements
            The path to a requirements.txt file

    Returns a list of modules that couldn't be imported
    """
    with Path(requirements).open() as fd:
        broken_modules = []

        for line in fd.readlines():
            line = line.strip().replace('<', '=').replace('>', '=')

            if len(line) == 0 or line[0] == '#' or line.startswith('-r'):
                continue

            if '#' in line:
                line = line.split('#')[0]

            module_name = line.split('=')[0] if '=' in line else line
            module_import_name = module_name.replace('-', '_')

            # Not every module is importable by its own name.
            if module_name == "pep8-naming":
                module_import_name = "pep8ext_naming"

            if not find_spec(module_import_name):
                broken_modules.append(module_name)

        return broken_modules


@lru_cache(maxsize=2)
def find_qmk_firmware():
    """Look for qmk_firmware in the usual places.

    This function returns the path to qmk_firmware, or the default location if one does not exist.
    """
    if in_qmk_firmware():
        return in_qmk_firmware()

    if cli.config.user.qmk_home:
        return Path(cli.config.user.qmk_home).expanduser().resolve()

    if 'QMK_HOME' in os.environ:
        path = Path(os.environ['QMK_HOME']).expanduser()
        if path.exists():
            return path.resolve()
        return path

    return Path.home() / 'qmk_firmware'


def in_qmk_firmware():
    """Returns the path to the qmk_firmware we are currently in, or None if we are not inside qmk_firmware.
    """
    cur_dir = Path.cwd()
    while len(cur_dir.parents) > 0:
        if is_qmk_firmware(cur_dir):
            return cur_dir

        # Move up a directory before the next iteration
        cur_dir = cur_dir / '..'
        cur_dir = cur_dir.resolve()
