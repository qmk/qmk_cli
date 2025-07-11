"""Clone a qmk_firmware fork.
"""
import os
from pathlib import Path

from milc import cli
from qmk_cli.git import git_clone
from qmk_cli.helpers import AbsPath

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('--baseurl', arg_only=True, default='https://github.com', help='The URL all git operations start from (Default: https://github.com)')
@cli.argument('-b', '--branch', arg_only=True, default=default_branch, help='The branch to clone. Default: %s' % default_branch)
@cli.argument('destination', arg_only=True, default=Path(os.environ['ORIG_CWD']) / default_repo, type=AbsPath, nargs='?', help='The directory to clone to. Default: (current directory)')
@cli.argument('fork', arg_only=True, default=default_fork, nargs='?', help='The qmk_firmware fork to clone. Default: %s' % default_fork)
@cli.subcommand('Clone a qmk_firmware fork.')
def clone(cli):
    git_url = '/'.join((cli.args.baseurl, cli.args.fork))

    # Exists (but not an empty dir)
    if cli.args.destination.exists() and any(cli.args.destination.iterdir()):
        cli.log.error('Destination already exists: %s', cli.args.destination)
        exit(1)

    return git_clone(git_url, cli.args.destination, cli.args.branch)
