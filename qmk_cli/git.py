"""Helpers for working with git."""

import subprocess
from .helpers import rmtree

from milc import cli

DEFAULT_UPSTREAM = 'https://github.com/qmk/qmk_firmware'


def git_clone(destination, url, branch):
    """Add the qmk/qmk_firmware upstream to a qmk_firmware clone."""
    git_clone = [
        'git',
        'clone',
        '--recurse-submodules',
        f'--branch={branch}',
        url,
        str(destination),
    ]
    cli.log.debug(f'Git clone command: {git_clone}')

    try:
        with subprocess.Popen(git_clone, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')

    except Exception as e:
        git_cmd = ' '.join([s.replace(' ', r'\ ') for s in git_clone])

        cli.log.error(f"Could not run '{git_cmd}': {e.__class__.__name__}:{e}")
        return False

    if p.returncode != 0:
        cli.log.error(f'git clone exited {p.returncode}')
        return False

    cli.log.info(f'Successfully cloned {url} to {destination}!')
    return True


def git_set_upstream(destination):
    """Add the qmk/qmk_firmware upstream to a qmk_firmware clone."""
    git_remote = [
        'git',
        '-C',
        str(destination),
        'remote',
        'add',
        'upstream',
        DEFAULT_UPSTREAM,
    ]
    cli.log.debug(f'Git remote command: {git_remote}')

    try:
        with subprocess.Popen(git_remote, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')

    except Exception as e:
        git_cmd = ' '.join([s.replace(' ', r'\ ') for s in git_remote])

        cli.log.error(f"Could not run '{git_cmd}': {e.__class__.__name__}:{e}")
        return False

    if p.returncode != 0:
        cli.log.error(f'git remote add exited {p.returncode}')
        return False

    cli.log.info(f'Added {DEFAULT_UPSTREAM} as remote upstream.')
    return True


def git_clone_fork(destination, baseurl, fork, branch, force=False):
    """Clone fork and configure upstream."""
    url = '/'.join((baseurl, fork))

    if force:
        rmtree(destination)

    if not git_clone(destination, url, branch):
        return False

    return git_set_upstream(destination)
