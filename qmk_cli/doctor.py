"""QMK Python Doctor

Check up for QMK environment.
"""
import shutil
import platform
import os
from pathlib import Path

from qmk_cli.milc import cli


def check_qmk_firmware():
    """Make sure qmk_firmware and the qmk cli are there.
    """
    qmk_firmware = Path(os.environ['QMK_HOME'])
    qmk_cli = qmk_firmware / 'bin' / 'qmk'

    if qmk_firmware.exists() and not qmk_cli.exists():
        cli.log.error("{fg_red}Can't find %s/bin/qmk! You need to `git pull`.", os.environ['QMK_HOME'])
        return False

    elif not qmk_firmware.exists():
        cli.log.error("{fg_red}Can't find the qmk_firmware checkout! %s does not exist!", os.environ['QMK_HOME'])
        return False

    cli.log.info('Found qmk_firmware checkout in {fg_cyan}%s', str(qmk_firmware))
    return True


def check_vital_programs():
    """Make sure the software we need has been installed.

    TODO(unclaimed):
        * [ ] Run the binaries to make sure they work
        * [ ] Compile a trivial program with each compiler
    """
    ok = True
    binaries = ['dfu-programmer', 'avrdude', 'dfu-util', 'avr-gcc', 'arm-none-eabi-gcc']

    for binary in binaries:
        res = shutil.which(binary)
        if res is None:
            cli.log.error("{fg_red}QMK can't find %s in your path", binary)
            ok = False

    if ok:
        cli.log.info("All necessary software is installed.")

    return ok


def check_platform_tests():
    """Dispatch to platform specific tests.
    """
    OS = platform.system()

    if OS == "Darwin":
        cli.log.info("Detected {fg_cyan}macOS")
        return check_mac_os()

    elif OS == "Linux":
        cli.log.info("Detected {fg_cyan}linux")
        return check_linux()

    else:
        cli.log.info("Assuming {fg_cyan}Windows")
        return check_windows()


def check_mac_os():
    """Run macOS specific tests.

    There aren't any yet.
    """
    return True


def check_linux():
    """Run Linux specific tests.

    TODO(unclaimed):
        * [ ] Check for udev entries on linux
    """
    test = 'systemctl list-unit-files | grep enabled | grep -i ModemManager'
    if os.system(test) == 0:
        cli.log.warn("{bg_yellow}Detected modem manager. Please disable it if you are using Pro Micros")


def check_windows():
    """Run Windows specific tests.

    TODO(unclaimed):
        * [ ] Check out the driver situation
    """
    return True
