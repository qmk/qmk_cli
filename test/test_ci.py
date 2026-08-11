import pytest
import subprocess


@pytest.fixture(autouse=True)
def temp_env(temp_directory, monkeypatch):
    qmk_firmware = temp_directory / 'qmk_firmware'
    monkeypatch.setenv("QMK_HOME", qmk_firmware.as_posix())
    yield qmk_firmware


@pytest.fixture
def run_cli(request):
    def run_cli_wrapper(args):
        cmd = f'{request.config.rootpath}/qmk' if request.config.getoption("--qmk") == 'wrapper' else 'qmk'

        return subprocess.run([cmd, *args], capture_output=True, text=True)

    return run_cli_wrapper


@pytest.mark.system
def test_cli_help(run_cli):
    completed_process = run_cli(['clone', '--help'])

    assert 'usage:' in completed_process.stdout
    assert completed_process.returncode == 0


@pytest.mark.system
def test_cli_setup_no(run_cli):
    completed_process = run_cli(['setup', '-n'])

    assert 'Could not find qmk_firmware!' in completed_process.stderr
    assert 'Not cloning qmk_firmware due to user input or --no flag.' in completed_process.stderr
    assert completed_process.returncode == 0


@pytest.mark.system
def test_cli_setup_yes(run_cli):
    completed_process = run_cli(['setup', '-y'])

    assert 'Successfully cloned https://github.com/qmk/qmk_firmware' in completed_process.stderr
    assert 'Added https://github.com/qmk/qmk_firmware as remote upstream' in completed_process.stderr
    assert 'QMK Doctor is checking your environment' in completed_process.stderr
    assert completed_process.returncode == 0
