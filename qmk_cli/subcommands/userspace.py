"""Setup qmk_userspace on your computer.
"""
import os
import sys
from pathlib import Path
from platformdirs import user_data_dir

from milc import cli

from milc.questions import yesno
from qmk_cli.git import git_clone
from qmk_cli.helpers import find_qmk_firmware, is_qmk_firmware, is_qmk_userspace

default_base = 'https://github.com'
default_fork = 'qmk/qmk_userspace'
default_branch = 'main'


@cli.argument('-n', '--no', arg_only=True, action='store_true', help='Answer no to all questions')
@cli.argument('-y', '--yes', arg_only=True, action='store_true', help='Answer yes to all questions')
@cli.argument('--baseurl', arg_only=True, default=default_base, help='The URL all git operations start from. Default: %s' % default_base)
@cli.argument('-b', '--branch', arg_only=True, default=default_branch, help='The branch to clone. Default: %s' % default_branch)
@cli.argument('-H', '--home', arg_only=True, default=Path(os.environ['QMK_USERSPACE']), type=Path, help='The location for qmk_userspace. Default: %s' % os.environ['QMK_HOME'])
@cli.argument('fork', arg_only=True, default=default_fork, nargs='?', help='The qmk_userspace fork to clone. Default: %s' % default_fork)
@cli.subcommand('Setup your computer for qmk_userspace.')
def userspace_setup(cli):
    """Guide the user through setting up their QMK environment.
    """
    # Sanity checks
    if cli.args.yes and cli.args.no:
        cli.log.error("Can't use both --yes and --no at the same time.")
        exit(1)

    if is_qmk_userspace(cli.args.home):
        cli.log.info(f'Found qmk_userspace at {cli.args.home}.')
    else: 
        cli.log.error('Could not find qmk_userspace!')
        if yesno('Would you like to clone qmk_userspace?'):
            git_url = f'{cli.args.baseurl}/{cli.args.fork}'
            if not git_clone(git_url, cli.args.home, cli.args.branch):
                exit(1)
        else:
            cli.log.warning('Not cloning qmk_userspace due to user input or --no flag.')

    qmk_firmware = find_qmk_firmware()
    if is_qmk_firmware(qmk_firmware):
        cli.log.info(f'Found qmk_firmware at {qmk_firmware}.')
    else: 
        cli.log.error('Could not find qmk_firmware!')
        if yesno('Would you like to clone qmk_firmware?'):
            git_url = f'{cli.args.baseurl}/qmk/qmk_firmware'
            hidden_home = Path(user_data_dir('qmk_cli', 'QMK')) / 'qmk_firmware'
            if not git_clone(git_url, hidden_home, 'master'):
                exit(1)
        else:
            cli.log.warning('Not cloning qmk_firmware due to user input or --no flag.')

    # Run `qmk doctor` to check the rest of the environment out
    if cli.args.home.exists():
        color = '--color' if cli.config.general.color else '--no-color'
        unicode = '--unicode' if cli.config.general.unicode else '--no-unicode'
        doctor_command = [Path(sys.argv[0]).as_posix(), color, unicode, 'doctor']

        if cli.args.no:
            doctor_command.append('-n')

        if cli.args.yes:
            doctor_command.append('-y')

        cli.run(doctor_command, stdin=None, capture_output=False, cwd=cli.args.home)
