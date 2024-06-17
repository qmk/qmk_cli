"""Installs python dependencies.
"""
import shlex
import shutil
import subprocess
from milc import cli

from qmk_cli.helpers import find_qmk_firmware, is_qmk_firmware


def _run_pip(pip_args, dry_run=False, upgrade=False):
    pip_exe = ['pip']
    if cli.config.user.pip_exe:
        pip_exe = shlex.split(cli.config.user.pip_exe)
    pip_command = [*pip_exe, *pip_args]
    pip_command[0] = shutil.which(pip_command[0])
    if shutil.which(pip_command[0]) is None:
        pip_command[0] = 'pip' # Hope falling back to unqualified path works

    if dry_run:
        print(" ".join(shlex.quote(str(s)) for s in pip_command))
        return True

    try:
        with subprocess.Popen(pip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')
    except Exception as e:
        pip_cmd = ' '.join([s.replace(' ', r'\ ') for s in pip_command])
        cli.log.error("Could not run '%s': %s: %s", pip_cmd, e.__class__.__name__, e)
        return False

    if p.returncode == 0:
        return True
    return False


def install_qmk_python_deps(upgrade=False, developer=False, dry_run=False):
    qmk_firmware_dir = find_qmk_firmware()
    if not is_qmk_firmware(qmk_firmware_dir):
        cli.log.error('Could not find {fg_cyan}qmk_firmware{fg_reset}!')
        return False

    reqs_path = qmk_firmware_dir / 'requirements.txt' if not developer else qmk_firmware_dir / 'requirements-dev.txt'

    pip_args = ['install', '-r', reqs_path]
    if upgrade:
        pip_args.append('--upgrade')

    if _run_pip(pip_args, dry_run=dry_run):
        if not dry_run:
            cli.log.info('Successfully installed python dependencies!')
        return True
    else:
        if not dry_run:
            cli.log.error('Failed to install python dependencies!')
        return False


@cli.argument('-u', '--upgrade', arg_only=True, action='store_true', help='Upgrades existing packages.')
@cli.argument('-d', '--developer', arg_only=True, action='store_true', help='Installs QMK Firmware developer dependencies, too.')
@cli.argument('-n', '--dry-run', arg_only=True, action='store_true', help='Prints the commands to execute, rather than executing them.')
@cli.subcommand('Installs python dependencies.')
def install_deps(cli):
    return install_qmk_python_deps(upgrade=cli.args.upgrade, developer=cli.args.developer, dry_run=cli.args.dry_run)


@cli.argument('-n', '--dry-run', arg_only=True, action='store_true', help='Prints the commands to execute, rather than executing them.')
@cli.argument('arguments', arg_only=True, default=[], nargs='*', help='The arguments to pass to pip.')
@cli.subcommand('Runs pip inside the qmk venv.')
def pip(cli):
    return _run_pip(cli.args.arguments, dry_run=cli.args.dry_run)
