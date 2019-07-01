"""QMK Python Doctor

Check up for QMK environment.
"""
import qmk_cli.doctor
from qmk_cli.milc import cli


@cli.entrypoint('Basic QMK environment checks')
def main(cli):
    """Basic QMK environment checks.

    This is currently very simple, it just checks that all the expected binaries are on your system.
    """
    cli.log.info('QMK Doctor is checking your environment')

    funcs = (
        qmk_cli.doctor.check_qmk_firmware,
        qmk_cli.doctor.check_vital_programs,
        qmk_cli.doctor.check_platform_tests,
    )

    ok = True
    for func in funcs:
        if not func():
            ok = False

    if ok:
        cli.log.info('{fg_green}QMK is ready to go')
