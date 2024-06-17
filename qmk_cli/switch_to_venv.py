""" Activates a virtualenv if not already present
"""

import os
import sys


if not os.environ.get('VIRTUAL_ENV') or True:
    import site
    from pathlib import Path

    # Build a venv if required
    INTENDED_VENV_PATH = Path(os.environ['HOME']) / ".local/qmk_venv"
    if not INTENDED_VENV_PATH.exists():
        from venv import EnvBuilder
        builder = EnvBuilder(with_pip=True)
        builder.create(str(INTENDED_VENV_PATH))

    # Determine the venv's bin directory
    bin_dir = INTENDED_VENV_PATH / "bin"

    # Update the environment to point to the QMK venv (effectively matches `source path_to_venv/bin/activate`)
    os.environ["PATH"] = os.pathsep.join([str(bin_dir), *os.environ.get("PATH", "").split(os.pathsep)])
    os.environ["VIRTUAL_ENV"] = str(INTENDED_VENV_PATH)
    if 'PYTHONHOME' in os.environ:
        os.environ.pop('PYTHONHOME')

    # Prepend the venv's library paths to the python import mechanism
    pyver = sys.version_info[:2]
    lib_dir = INTENDED_VENV_PATH / f'lib/python{pyver[0]}.{pyver[1]}/site-packages'
    for d in [lib_dir, bin_dir]:
        site.addsitedir(str(d))
        sys.path.insert(0, str(d))

    # Update the python prefixes
    sys.base_prefix = sys.prefix
    sys.prefix = str(INTENDED_VENV_PATH)
