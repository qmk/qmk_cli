import pytest
import subprocess
from unittest.mock import patch, PropertyMock

import qmk_cli.git


@patch("qmk_cli.git.subprocess.Popen", side_effect=Exception("foobar"))
@patch("qmk_cli.git.cli.log.error")
def test_git_clone_except(mock_log_error, mock_popen):
    ret = qmk_cli.git.git_clone('/tmp', 'https://github.com/qmk/qmk_firmware', 'master')

    assert "Could not run" in str(mock_log_error.call_args_list)
    assert "Exception:foobar" in str(mock_log_error.call_args_list)
    assert ret is False


@patch("qmk_cli.git.subprocess.Popen")
def test_git_clone_logs_output(mock_popen, capsys):
    type(mock_popen().__enter__()).returncode = PropertyMock(return_value=0)
    type(mock_popen().__enter__()).stdout = PropertyMock(return_value=['asdf'])

    ret = qmk_cli.git.git_clone('/tmp', 'https://github.com/qmk/qmk_firmware', 'master')

    captured = capsys.readouterr().out
    assert 'asdf' in captured
    assert ret is True


@patch("qmk_cli.git.subprocess.Popen")
def test_git_clone_captures_exit_code(mock_popen):
    type(mock_popen().__enter__()).returncode = PropertyMock(return_value=1)

    ret = qmk_cli.git.git_clone('/tmp', 'https://github.com/qmk/qmk_firmware', 'master')

    assert ret is False


@patch("qmk_cli.git.subprocess.Popen", side_effect=Exception("foobar"))
@patch("qmk_cli.git.cli.log.error")
def test_git_set_upstream_except(mock_log_error, mock_popen):
    ret = qmk_cli.git.git_set_upstream('/tmp')

    assert "Could not run" in str(mock_log_error.call_args_list)
    assert "Exception:foobar" in str(mock_log_error.call_args_list)
    assert ret is False


@patch("qmk_cli.git.subprocess.Popen")
def test_git_set_upstream_logs_output(mock_popen, capsys):
    type(mock_popen().__enter__()).returncode = PropertyMock(return_value=0)
    type(mock_popen().__enter__()).stdout = PropertyMock(return_value=['asdf'])

    ret = qmk_cli.git.git_set_upstream('/tmp')

    captured = capsys.readouterr().out
    assert 'asdf' in captured
    assert ret is True


@patch("qmk_cli.git.subprocess.Popen")
def test_git_set_upstream_captures_exit_code(mock_popen):
    type(mock_popen().__enter__()).returncode = PropertyMock(return_value=1)

    ret = qmk_cli.git.git_set_upstream('/tmp')

    assert ret is False


@patch.object(qmk_cli.git, 'git_clone')
@patch.object(qmk_cli.git, 'git_set_upstream')
def test_git_clone_fork_fail(git_set_upstream, git_clone, temp_directory):
    git_clone.return_value = False
    git_set_upstream.return_value = False

    ret = qmk_cli.git.git_clone_fork(temp_directory.as_posix(), 'https://github.com', 'qmk/qmk_firmware', 'master', False)

    assert ret is False


@patch.object(qmk_cli.git, 'git_clone')
@patch.object(qmk_cli.git, 'git_set_upstream')
def test_git_clone_fork_force(git_set_upstream, git_clone, temp_directory):
    (temp_directory / 'asdf').touch()

    git_clone.return_value = True
    git_set_upstream.return_value = True

    ret = qmk_cli.git.git_clone_fork(temp_directory.as_posix(), 'https://github.com', 'qmk/qmk_firmware', 'master', True)

    assert ret is True
    assert (temp_directory / 'asdf').exists() is False


@pytest.mark.integration
def test_git_clone(temp_directory):
    qmk_firmware = temp_directory / 'qmk_firmware'
    ret = qmk_cli.git.git_clone(qmk_firmware.as_posix(), 'https://github.com/qmk/qmk_firmware', 'master')

    from qmk_cli.helpers import is_qmk_firmware

    assert is_qmk_firmware(qmk_firmware) is True
    assert ret is True


@pytest.mark.integration
def test_git_clone_fork(temp_directory):
    qmk_firmware = temp_directory / 'qmk_firmware'
    qmk_firmware.mkdir()
    (qmk_firmware / 'asdf').touch()
    ret = qmk_cli.git.git_clone_fork(qmk_firmware.as_posix(), 'https://github.com', 'qmk/qmk_firmware', 'master', True)

    from qmk_cli.helpers import is_qmk_firmware

    assert is_qmk_firmware(qmk_firmware) is True
    assert 'https://github.com/qmk/qmk_firmware' in subprocess.run(['git', '-C', qmk_firmware.as_posix(), 'remote', 'get-url', 'upstream'], capture_output=True, text=True).stdout
    assert ret is True
