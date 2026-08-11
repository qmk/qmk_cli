import pytest
from unittest.mock import patch, PropertyMock, ANY


@pytest.fixture
def subcommand(temp_directory):
    tmp = temp_directory.as_posix()
    with patch.dict('os.environ', {'ORIG_CWD': tmp, 'QMK_HOME': tmp}, clear=True):
        import qmk_cli.subcommands.setup as setup

        yield setup


@pytest.fixture
def is_qmk_firmware(subcommand):
    with patch.object(subcommand, 'is_qmk_firmware') as is_qmk_firmware:
        is_qmk_firmware.return_value = True

        yield is_qmk_firmware


@pytest.fixture
def yesno(subcommand):
    with patch.object(subcommand, 'yesno') as yesno:
        yesno.return_value = True

        yield yesno


@pytest.fixture
def choice(subcommand):
    with patch.object(subcommand, 'choice') as choice:
        yield choice


@pytest.fixture
def question(subcommand):
    with patch.object(subcommand, 'question') as question:
        yield question


@pytest.fixture
def git_clone_fork(subcommand):
    with patch.object(subcommand, 'git_clone_fork') as git_clone_fork:
        yield git_clone_fork


def test_setup_both_yes_no_invalid(subcommand, mock_cli):
    type(mock_cli.args).yes = PropertyMock(return_value=True)
    type(mock_cli.args).no = PropertyMock(return_value=True)

    ret = subcommand.setup(mock_cli)

    assert ret is False


def test_setup_reclone(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    type(mock_cli.args).fork = 'asdf'
    choice.return_value = 'Delete and reclone asdf'
    yesno.return_value = True

    subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'This will delete your current qmk_firmware directory.' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()


def test_setup_reclone_failed(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    type(mock_cli.args).fork = 'asdf'
    choice.return_value = 'Delete and reclone asdf'
    yesno.return_value = True
    git_clone_fork.return_value = False

    ret = subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'This will delete your current qmk_firmware directory.' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()
    assert ret is False


def test_setup_reclone_no(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    type(mock_cli.args).fork = 'asdf'
    choice.return_value = 'Delete and reclone asdf'
    yesno.return_value = False

    ret = subcommand.setup(mock_cli)

    assert ret is False
    git_clone_fork.assert_not_called()


def test_setup_clone_diff_fork(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, question, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    choice.return_value = 'Delete and clone a different fork'
    yesno.return_value = True

    subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'This will delete your current qmk_firmware directory.' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()


def test_setup_clone_diff_fork_failed(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, question, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    choice.return_value = 'Delete and clone a different fork'
    yesno.return_value = True
    git_clone_fork.return_value = False

    ret = subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'This will delete your current qmk_firmware directory.' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()
    assert ret is False


def test_setup_clone_diff_fork_no(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, choice, question, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    choice.return_value = 'Delete and clone a different fork'
    yesno.return_value = False

    ret = subcommand.setup(mock_cli)

    assert ret is False
    git_clone_fork.assert_not_called()


def test_setup_home_exists_not_empty(subcommand, mock_cli, is_qmk_firmware, temp_directory):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    is_qmk_firmware.return_value = False
    (temp_directory / 'asdf').touch()

    ret = subcommand.setup(mock_cli)

    assert ret is False


def test_setup_missing(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    is_qmk_firmware.return_value = False
    yesno.return_value = True

    subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'Would you like to clone' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()


def test_setup_missing_failed(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    is_qmk_firmware.return_value = False
    yesno.return_value = True
    git_clone_fork.return_value = False

    ret = subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'Would you like to clone' in yesno.call_args.args[0]
    git_clone_fork.assert_called_once()
    assert ret is False


def test_setup_missing_no(subcommand, mock_cli, is_qmk_firmware, temp_directory, yesno, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=False)
    type(mock_cli.args).home = PropertyMock(return_value=temp_directory)
    is_qmk_firmware.return_value = False
    yesno.return_value = False

    subcommand.setup(mock_cli)

    yesno.assert_called_once()
    assert 'Would you like to clone' in yesno.call_args.args[0]
    git_clone_fork.assert_not_called()


def test_setup_chains_args_to_doctor(subcommand, mock_cli, is_qmk_firmware, yesno, choice, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=True)
    type(mock_cli.args).no = PropertyMock(return_value=False)

    subcommand.setup(mock_cli)

    mock_cli.run.assert_called_once()
    assert mock_cli.run.call_args.args[0] == [ANY, '--color', '--unicode', 'doctor', '-y']


def test_setup_chains_args_to_doctor_no(subcommand, mock_cli, is_qmk_firmware, yesno, choice, git_clone_fork):
    type(mock_cli.args).yes = PropertyMock(return_value=False)
    type(mock_cli.args).no = PropertyMock(return_value=True)
    mock_cli.config.general.color = False
    mock_cli.config.general.unicode = False

    subcommand.setup(mock_cli)

    mock_cli.run.assert_called_once()
    assert mock_cli.run.call_args.args[0] == [ANY, '--no-color', '--no-unicode', 'doctor', '-n']
