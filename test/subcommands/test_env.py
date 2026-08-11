import pytest
from unittest.mock import patch, PropertyMock


@pytest.fixture
def subcommand(temp_directory):
    tmp = temp_directory.as_posix()
    with patch.dict('os.environ', {'ORIG_CWD': tmp, 'QMK_HOME': tmp}, clear=True):
        import qmk_cli.subcommands.env as env

        yield env


@pytest.fixture
def is_qmk_firmware(subcommand):
    with patch.object(subcommand, 'is_qmk_firmware') as is_qmk_firmware:
        is_qmk_firmware.return_value = True

        yield is_qmk_firmware


def test_request_qmk_firmware_exists(subcommand, mock_cli, capsys, temp_directory, is_qmk_firmware):
    subcommand.env(mock_cli)
    captured = capsys.readouterr().out
    assert f'QMK_HOME="{temp_directory}"' in captured
    assert f'QMK_FIRMWARE="{temp_directory}"' in captured


def test_request_all_variables(subcommand, mock_cli, capsys, temp_directory):
    subcommand.env(mock_cli)
    captured = capsys.readouterr().out
    assert f'QMK_HOME="{temp_directory}"' in captured
    assert 'QMK_FIRMWARE=""' in captured
    assert 'QMK_UNICODE="True"' in captured


def test_request_single_variable(subcommand, mock_cli, capsys, temp_directory):
    type(mock_cli.args).var = PropertyMock(return_value='QMK_HOME')

    subcommand.env(mock_cli)
    captured = capsys.readouterr().out
    assert captured == f'{temp_directory}\n'


def test_request_single_variable_no_exits(subcommand, mock_cli, capsys):
    type(mock_cli.args).var = PropertyMock(return_value='ASDF')

    ret = subcommand.env(mock_cli)
    captured = capsys.readouterr().err
    assert captured == 'Variable "ASDF" does not exist!\n'
    assert ret is False
