"""Clone a qmk_firmware fork.
"""
import os
from pathlib import Path

from qmk_cli.milc import cli
from qmk.cli.git import clone

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
    git_url = '/'.join((cli.config.general.baseurl, cli.args.fork))

    if qmk_firmware.exists():
        cli.log.error('Destination already exists: %s', cli.args.destination)
        exit(1)

    success = clone(git_url, cli.args.destination, cli.config.general.branch)
    exit(0 if success else 1)
