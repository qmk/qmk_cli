import pytest
from unittest.mock import patch, PropertyMock


@pytest.fixture
def subcommand(temp_directory):
    tmp = temp_directory.as_posix()
    with patch.dict('os.environ', {'ORIG_CWD': tmp, 'QMK_HOME': tmp}, clear=True):
        import qmk_cli.subcommands.clone as clone

        yield clone


@pytest.fixture
def git_clone(subcommand):
    with patch.object(subcommand, 'git_clone') as git_clone:
        yield git_clone


def test_clone(subcommand, mock_cli, git_clone):
    type(mock_cli.args).baseurl = PropertyMock(return_value='asdf')
    type(mock_cli.args).fork = PropertyMock(return_value='fork')
    git_clone.return_value = True

    ret = subcommand.clone(mock_cli)

    git_clone.assert_called_once()
    assert ret is True


def test_clone_not_empty(subcommand, mock_cli, temp_directory, git_clone):
    type(mock_cli.args).baseurl = PropertyMock(return_value='asdf')
    type(mock_cli.args).fork = PropertyMock(return_value='fork')
    type(mock_cli.args).destination = PropertyMock(return_value=temp_directory)
    (temp_directory / 'asdf').touch()

    ret = subcommand.clone(mock_cli)

    git_clone.assert_not_called()
    assert ret is False
