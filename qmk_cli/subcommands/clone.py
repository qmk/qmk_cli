"""Clone a qmk_firmware fork.
"""
import os
from pathlib import Path

from milc import cli
from qmk_cli.git import git_clone

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from (Default: https://github.com)')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone. Default: %s' % default_branch)
@cli.argument('destination', default=None, nargs='?', help='The directory to clone to. Default: (current directory)')
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone. Default: %s' % default_fork)
@cli.subcommand('Clone a qmk_firmware fork.')
def clone(cli):
    if not cli.args.destination:
        cli.args.destination = os.path.join(os.environ['ORIG_CWD'], default_fork.split('/')[-1])

    qmk_firmware = Path(cli.args.destination)
    git_url = '/'.join((cli.config.clone.baseurl, cli.args.fork))

    if qmk_firmware.exists():
        cli.log.error('Destination already exists: %s', cli.args.destination)
        exit(1)

    return git_clone(git_url, cli.args.destination, cli.config.clone.branch)
