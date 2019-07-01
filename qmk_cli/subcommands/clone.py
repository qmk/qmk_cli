"""Clone a qmk_firmware fork.
"""
import os
import subprocess
from pathlib import Path

from qmk_cli.milc import cli

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'

@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from.')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone.')
@cli.argument('destination', default=os.environ['QMK_HOME'], nargs='?', help='The directory to clone to.')
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone')
@cli.entrypoint('Clone a qmk_firmware fork.')
def main(cli):
    qmk_firmware = Path(cli.args.destination)
    git_clone = [
        'git',
        'clone',
        '--recurse-submodules',
        '--branch=' + cli.config.general.branch,
        '/'.join((cli.config.general.baseurl, cli.args.fork)),
        cli.args.destination,
    ]

    if qmk_firmware.exists():
        cli.log.error('Destination already exists: %s', cli.args.destination)
        exit(1)

    with subprocess.Popen(git_clone, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode != 0:
        cli.log.error('git clone exited %d', p.returncode)
    else:
        cli.log.info('Successfully cloned %s to %s!', cli.args.fork, cli.args.destination)
