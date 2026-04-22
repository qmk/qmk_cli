"""Helpers for working with git.
"""
import subprocess

from milc import cli


def git_clone(url, destination, branch):
    git_clone = [
        'git',
        'clone',
        '--recurse-submodules',
        '--branch=' + branch,
        url,
        str(destination),
    ]
    cli.log.debug(f'Git clone command: {git_clone}', )

    try:
        with subprocess.Popen(git_clone, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')

    except Exception as e:
        git_cmd = ' '.join([s.replace(' ', r'\ ') for s in git_clone])

        cli.log.error(f'Could not run "{git_cmd}": {e.__class__}: {e}')
        return False

    if p.returncode != 0:
        cli.log.error(f'git clone exited {p.returncode}')
        return False

    cli.log.info(f'Successfully cloned {url} to {destination}!')
    return True
