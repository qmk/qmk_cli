"""Setup qmk_firmware on your computer.
"""
import os
import subprocess
from pathlib import Path

from qmk_cli.doctor import check_vital_programs
from qmk_cli.git import clone
from qmk_cli.helpers import question
from qmk_cli.milc import cli

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('-y', '--yes', action='store_true', help='Answer yes to all questions')
@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone')
@cli.argument('destination', default=os.environ['QMK_HOME'], nargs='?', help='The directory to clone to')
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone')
@cli.entrypoint('Setup your computer for qmk_firmware.')
def main(cli):
    qmk_firmware = Path(cli.args.destination)

    # Check on qmk_firmware, and if it doesn't exist offer to check it out.
    if qmk_firmware.exists():
        cli.log.info('Found qmk_firmware at %s.', str(qmk_firmware))
    else:
        if question('Would you like to clone %s?' % cli.args.fork):
            git_url = '/'.join((cli.config.general.baseurl, cli.args.fork))
            clone(git_url, cli.args.destination, cli.config.general.branch)

    # Check if the build environment is setup, and if not offer to set it up
    if not check_vital_programs():
        cli.log.info('Your build environment is not setup completely.')
        if question('Would you like to run util/qmk_install?'):
            curdir = os.getcwd()
            os.chdir(str(qmk_firmware))
            subprocess.run(['util/qmk_install.sh'])
            os.chdir(curdir)

    # fin
    cli.log.info('QMK setup complete!')
