"""Helpers for working with git.
"""
import subprocess

from milc import cli

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


def clone(url, destination, branch):
    git_clone = [
        'git',
        'clone',
        '--recurse-submodules',
        '--branch=' + branch,
        url,
        destination,
    ]
    cli.log.debug('Git clone command: %s', git_clone)

    with subprocess.Popen(git_clone, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode != 0:
        cli.log.error('git clone exited %d', p.returncode)
        return False
    else:
        cli.log.info('Successfully cloned %s to %s!', cli.args.fork, cli.args.destination)
        return True
