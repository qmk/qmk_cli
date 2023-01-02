"""Helpers for working with git.
"""
import subprocess

from milc import cli

default_repo = 'qmk_firmware'
default_fork = 'qmk/' + default_repo
default_branch = 'master'


def git_clone(url, destination, branch):
    git_clone = [
        'git',
        'clone',
        '--recurse-submodules',
        '--branch=' + branch,
        url,
        str(destination),
    ]
    cli.log.debug('Git clone command: %s', git_clone)

    try:
        with subprocess.Popen(git_clone, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')

    except Exception as e:
        git_cmd = ' '.join([s.replace(' ', r'\ ') for s in git_clone])

        cli.log.error("Could not run '%s': %s: %s", git_cmd, e.__class__.__name__, e)
        return False

    if p.returncode == 0:
        cli.log.info('Successfully cloned %s to %s!', url, destination)
        return True

    else:
        cli.log.error('git clone exited %d', p.returncode)
        return False


def git_init(destination, branch):
    git_clone = [
        'git',
        'init',
        '--initial-branch=' + branch,
        str(destination),
    ]
    cli.log.debug('Git clone command: %s', git_clone)

    try:
        with subprocess.Popen(git_clone, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
            for line in p.stdout:
                print(line, end='')

    except Exception as e:
        git_cmd = ' '.join([s.replace(' ', r'\ ') for s in git_clone])

        cli.log.error("Could not run '%s': %s: %s", git_cmd, e.__class__.__name__, e)
        return False

    if p.returncode == 0:
        cli.log.info('Successfully init-ed %s!', destination)
        return True

    else:
        cli.log.error('git init exited %d', p.returncode)
        return False


def git_upstream(destination, baseurl, default_fork, name):
    """Add the qmk/qmk_firmware upstream to a qmk_firmware clone.
    """
    git_url = '/'.join((baseurl, default_fork))
    git_cmd = [
        'git',
        '-C',
        destination,
        'remote',
        'add',
        name,
        git_url,
    ]

    with subprocess.Popen(git_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8') as p:
        for line in p.stdout:
            print(line, end='')

    if p.returncode == 0:
        cli.log.info('Added %s as remote %s.', git_url, name)
        return True
    else:
        cli.log.error('%s exited %d', ' '.join(git_cmd), p.returncode)
        return False


def git_check_repo(destination):
    """Checks that the .git directory exists.

    This is a decent enough indicator that the qmk_firmware directory is a
    proper Git repository, rather than a .zip download from GitHub.
    """
    dot_git_dir = destination / '.git'

    return dot_git_dir.is_dir()
