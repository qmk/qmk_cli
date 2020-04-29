"""Setup qmk_firmware on your computer.
"""
import os
import shlex
import subprocess
import sys
from pathlib import Path

from milc import cli
from qmk_cli.git import git_clone
from qmk_cli.helpers import question

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


@cli.argument('-n', '--no', arg_only=True, action='store_true', help='Answer no to all questions')
@cli.argument('-y', '--yes', arg_only=True, action='store_true', help='Answer yes to all questions')
@cli.argument('--baseurl', default='https://github.com', help='The URL all git operations start from')
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone')
@cli.argument('-H', '--home', default=Path(os.environ['QMK_HOME']), type=Path, help='The location for QMK Firmware. Defaults to %s' % (os.environ['QMK_HOME'],))
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone')
@cli.subcommand('Setup your computer for qmk_firmware.')
def setup(cli):
    """Guide the user through setting up their QMK environment.
    """
    clone_prompt = 'Would you like to clone {fg_cyan}%s{fg_reset} to {fg_cyan}%s{fg_reset}?' % (cli.args.fork, shlex.quote(str(cli.args.home)))
    home_prompt = 'Would you like to set {fg_cyan}%s{fg_reset} as your QMK home?' % (shlex.quote(str(cli.args.home)),)

    # Sanity checks
    if cli.args.yes and cli.args.no:
        cli.log.error("Can't use both --yes and --no at the same time.")
        exit(1)

    # Check on qmk_firmware, and if it doesn't exist offer to check it out.
    if (cli.args.home / 'Makefile').exists():
        cli.log.info('Found qmk_firmware at %s.', str(cli.args.home))
    else:
        cli.log.error('Could not find qmk_firmware!')
        if question(clone_prompt):
            git_url = '/'.join((cli.config.setup.baseurl, cli.args.fork))
            result = git_clone(git_url, cli.args.home, cli.config.setup.branch)
            if result != 0:
                exit(1)

    # Offer to set `user.qmk_home` for them.
    if cli.args.home != os.environ['QMK_HOME'] and question(home_prompt):
        cli.config['user']['qmk_home'] = str(cli.args.home.absolute())
        cli.write_config_option('user', 'qmk_home')

    # Run `qmk_firmware/bin/qmk doctor` to check the rest of the environment out
    qmk_bin = cli.args.home / 'bin/qmk'
    doctor_cmd = [sys.executable, qmk_bin, 'doctor']

    if cli.args.yes:
        doctor_cmd.append('--yes')

    if cli.args.no:
        doctor_cmd.append('--no')

    subprocess.run(doctor_cmd)
