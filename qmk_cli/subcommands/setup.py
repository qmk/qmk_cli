"""Setup qmk_firmware on your computer.
"""
import os
import shlex
import subprocess
import sys
from pathlib import Path

from milc import cli
from milc.questions import yesno
from qmk_cli.git import git_clone

default_base = 'https://github.com'
default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


def git_upstream(destination):
    """Add the qmk/qmk_firmware upstream to a qmk_firmware clone.
    """
    git_url = '/'.join((cli.config.setup.baseurl, default_fork))
    git_cmd = [
        'git',
        '-C',
        destination,
        'remote',
        'add',
        'upstream',
        git_url,
    ]

    with subprocess.Popen(git_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode == 0:
        cli.log.info('Added %s as remote upstream.', git_url)
        return True
    else:
        cli.log.error('%s exited %d', ' '.join(git_cmd), p.returncode)
        return False


def is_qmk_firmware(qmk_firmware):
    """Returns True if the given Path() is a qmk_firmware clone.
    """
    paths = [
        qmk_firmware,
        qmk_firmware / 'Makefile',
        qmk_firmware / 'requirements.txt',
        qmk_firmware / 'requirements-dev.txt',
        qmk_firmware / 'lib/python/qmk/cli/doctor.py'
    ]

    for path in paths:
        if not path.exists():
            cli.log.error('%s is not a qmk_firmware clone!', str(qmk_firmware))
            return False

    return True


@cli.argument('-n', '--no', arg_only=True, action='store_true', help='Answer no to all questions')
@cli.argument('-y', '--yes', arg_only=True, action='store_true', help='Answer yes to all questions')
@cli.argument('--baseurl', default=default_base, help='The URL all git operations start from. Default: %s' % default_base)
@cli.argument('-b', '--branch', default=default_branch, help='The branch to clone. Default: %s' % default_branch)
@cli.argument('-H', '--home', default=Path(os.environ['QMK_HOME']), type=Path, help='The location for QMK Firmware. Default: %s' % os.environ['QMK_HOME'])
@cli.argument('fork', default=default_fork, nargs='?', help='The qmk_firmware fork to clone. Default: %s' % default_fork)
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
    if is_qmk_firmware(cli.args.home):
        cli.log.info('Found qmk_firmware at %s.', str(cli.args.home))

    elif qmk_firmware.exists():
        path_str = str(qmk_firmware)

        if qmk_firmware.name != 'qmk_firmware':
            cli.log.warning('Warning: %s does not end in "qmk_firmware". Did you mean to use "--home %s/qmk_firmware"?' % (path_str, path_str))

        cli.log.error("Path '%s' exists but is not a qmk_firmware clone!", path_str)
        exit(1)

    else:
        cli.log.error('Could not find qmk_firmware!')
        if yesno(clone_prompt):
            git_url = '/'.join((cli.config.setup.baseurl, cli.args.fork))

            if git_clone(git_url, cli.args.home, cli.config.setup.branch):
                git_upstream(cli.args.home)
            else:
                exit(1)

    # Offer to set `user.qmk_home` for them.
    if str(cli.args.home) != os.environ['QMK_HOME'] and yesno(home_prompt):
        cli.config['user']['qmk_home'] = str(cli.args.home.absolute())
        cli.write_config_option('user', 'qmk_home')

    # Run `qmk doctor` to check the rest of the environment out
    doctor_command = [sys.executable, sys.argv[0], 'doctor']

    if cli.args.no:
        doctor_command.append('--no')

    if cli.args.yes:
        doctor_command.append('--yes')

    cli.run(doctor_command, capture_output=False)
