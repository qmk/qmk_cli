"""Setup qmk_firmware on your computer.
"""
import os
import subprocess
import sys
from pathlib import Path

from milc import cli
from qmk_cli.git import clone
from qmk_cli.helpers import question

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('-n', '--no', arg_only=True, action='store_true', help='Answer no to all questions')
@cli.argument('-y', '--yes', arg_only=True, action='store_true', help='Answer yes to all questions')
@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone')
@cli.argument('destination', default=os.environ['QMK_HOME'], nargs='?', help='The directory to clone to')
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone')
@cli.subcommand('Setup your computer for qmk_firmware.')
def setup(cli):
    qmk_firmware = Path(cli.args.destination)

    # Sanity checks
    if cli.args.yes and cli.args.no:
        cli.log.error("Can't use both --yes and --no at the same time.")
        exit(1)

    # Check on qmk_firmware, and if it doesn't exist offer to check it out.
    if (qmk_firmware / 'Makefile').exists():
        cli.log.info('Found qmk_firmware at %s.', str(qmk_firmware))
    else:
        cli.log.error('qmk_firmware not found!')
        if question('Would you like to clone %s?' % cli.args.fork):
            git_url = '/'.join((cli.config.setup.baseurl, cli.args.fork))
            clone(git_url, cli.args.destination, cli.config.setup.branch)

    # Run `qmk_firmware/bin/qmk doctor` to check the rest of the environment out
    if qmk_firmware.exists():
        qmk_bin = qmk_firmware / 'bin' / 'qmk'
        doctor_cmd = [sys.executable, str(qmk_bin), 'doctor']
        if cli.args.yes:
            doctor_cmd.append('--yes')
        if cli.args.no:
            doctor_cmd.append('--no')
        doctor = subprocess.run(doctor_cmd)
        if doctor.returncode != 0:
            cli.log.error('Your build environment is not setup completely.')

            if question('Would you like to run util/qmk_install?'):
                curdir = os.getcwd()
                os.chdir(str(qmk_firmware))
                process = subprocess.run(['util/qmk_install.sh'])
                os.chdir(curdir)
                if process.returncode == 0:
                    cli.log.info('QMK setup complete!')
