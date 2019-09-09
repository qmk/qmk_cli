"""Clone a qmk_firmware fork.
"""
import os
from pathlib import Path

from milc import cli
from qmk_cli.git import clone

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from.')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone.')
@cli.argument('destination', default=os.environ['QMK_HOME'], nargs='?', help='The directory to clone to.')
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone')
@cli.subcommand('Clone a qmk_firmware fork.')
def clone(cli):
    qmk_firmware = Path(cli.args.destination)
    git_url = '/'.join((cli.config.clone.baseurl, cli.args.fork))

    if qmk_firmware.exists():
        cli.log.error('Destination already exists: %s', cli.args.destination)
        exit(1)

    success = clone(git_url, cli.args.destination, cli.config.clone.branch)
    exit(0 if success else 1)
