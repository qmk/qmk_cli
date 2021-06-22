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
        qmk_firmware / 'lib/python/qmk/cli/__init__.py'
    ]

    for path in paths:
        if not path.exists():
            return False

    return True


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
