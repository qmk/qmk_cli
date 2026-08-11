import os
import stat
import pytest
from pathlib import Path
from unittest.mock import patch, PropertyMock

import qmk_cli.helpers


@pytest.fixture(autouse=True)
def reset_env():
    cur_dir = os.getcwd()

    yield cur_dir

    os.chdir(cur_dir)
    qmk_cli.helpers.find_qmk_firmware.cache_clear()
    qmk_cli.helpers.in_qmk_firmware.cache_clear()
    qmk_cli.helpers.find_qmk_userspace.cache_clear()
    qmk_cli.helpers.in_qmk_userspace.cache_clear()


def test_abspath(temp_directory):
    tmp = temp_directory.absolute()
    ret = qmk_cli.helpers.AbsPath(tmp)
    assert ret.samefile(tmp)


def test_abspath_str(temp_directory):
    tmp = temp_directory.absolute().as_posix()
    ret = qmk_cli.helpers.AbsPath(tmp)
    assert ret.samefile(tmp)


def test_abspath_rel(temp_directory):
    with patch.dict('os.environ', {'ORIG_CWD': temp_directory.as_posix()}, clear=True):
        tmp = './asdf'
        ret = qmk_cli.helpers.AbsPath(tmp)
        assert ret.as_posix() == (temp_directory / 'asdf').as_posix()


def test_rmtree(temp_directory):
    tmp = temp_directory / 'asdf.txt'
    tmp.touch()

    qmk_cli.helpers.rmtree(temp_directory)

    assert tmp.exists() is False


@pytest.mark.skipif(os.name != "nt", reason="Only triggers issue on windows")
def test_rmtree_readonly(temp_directory):
    tmp = temp_directory / 'asdf.txt'
    tmp.touch()
    os.chmod(tmp, stat.S_IREAD)

    qmk_cli.helpers.rmtree(temp_directory)

    assert tmp.exists() is False


def test_is_qmk_firmware(temp_directory):
    (temp_directory / 'quantum').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'requirements.txt').touch()
    (temp_directory / 'requirements-dev.txt').touch()
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()

    assert qmk_cli.helpers.is_qmk_firmware(temp_directory) is True


def test_is_qmk_firmware_partially_missing(temp_directory):
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()

    assert qmk_cli.helpers.is_qmk_firmware(temp_directory) is False


def test_find_qmk_firmware(temp_directory):
    (temp_directory / 'quantum').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'requirements.txt').touch()
    (temp_directory / 'requirements-dev.txt').touch()
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()
    os.chdir(temp_directory)

    assert qmk_cli.helpers.find_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_find_qmk_firmware_env(temp_directory):
    with patch.dict('os.environ', {'QMK_HOME': temp_directory.as_posix()}, clear=True):
        assert qmk_cli.helpers.find_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_find_qmk_firmware_env_missing(temp_directory):
    with patch.dict('os.environ', {'QMK_HOME': (temp_directory / 'asdf').as_posix()}, clear=True):
        assert qmk_cli.helpers.find_qmk_firmware().as_posix() == (temp_directory / 'asdf').as_posix()


def test_find_qmk_firmware_config(temp_directory):
    with patch.object(qmk_cli.helpers, 'cli') as cli:
        type(cli.config.user).qmk_home = PropertyMock(return_value=temp_directory.as_posix())

        assert qmk_cli.helpers.find_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_find_qmk_firmware_config_user():
    with patch.object(qmk_cli.helpers, 'cli') as cli:
        type(cli.config.user).qmk_home = PropertyMock(return_value='~/asdf')

        assert qmk_cli.helpers.find_qmk_firmware().as_posix() == (Path.home() / 'asdf').as_posix()


def test_find_qmk_firmware_default(temp_directory):
    with patch('pathlib.Path.home') as home:
        home.return_value = temp_directory

        assert qmk_cli.helpers.find_qmk_firmware().as_posix() == (temp_directory / 'qmk_firmware').as_posix()


def test_in_qmk_firmware(temp_directory):
    (temp_directory / 'quantum').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'requirements.txt').touch()
    (temp_directory / 'requirements-dev.txt').touch()
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()
    os.chdir(temp_directory)

    assert qmk_cli.helpers.in_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_in_qmk_firmware_sub(temp_directory):
    (temp_directory / 'quantum').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'requirements.txt').touch()
    (temp_directory / 'requirements-dev.txt').touch()
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()
    os.chdir(temp_directory / 'quantum')

    assert qmk_cli.helpers.in_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_in_qmk_firmware_sub_sub(temp_directory):
    (temp_directory / 'quantum').mkdir(parents=True)
    (temp_directory / 'lib/python/qmk/cli').mkdir(parents=True)
    (temp_directory / 'requirements.txt').touch()
    (temp_directory / 'requirements-dev.txt').touch()
    (temp_directory / 'lib/python/qmk/cli/__init__.py').touch()
    os.chdir(temp_directory / 'lib' / 'python')

    assert qmk_cli.helpers.in_qmk_firmware().as_posix() == temp_directory.as_posix()


def test_in_qmk_firmware_invalid(temp_directory):
    os.chdir(temp_directory)

    assert qmk_cli.helpers.in_qmk_firmware() is None


def test_is_qmk_userspace(temp_directory):
    (temp_directory / 'qmk.json').write_text('{"userspace_version": 2}')

    assert qmk_cli.helpers.is_qmk_userspace(temp_directory) is True


def test_is_qmk_userspace_missing(temp_directory):
    assert qmk_cli.helpers.is_qmk_userspace(temp_directory) is False


def test_is_qmk_userspace_invalid(temp_directory):
    (temp_directory / 'qmk.json').write_text('asdf')

    assert qmk_cli.helpers.is_qmk_userspace(temp_directory) is False


def test_is_qmk_userspace_empty(temp_directory):
    (temp_directory / 'qmk.json').touch()

    assert qmk_cli.helpers.is_qmk_userspace(temp_directory) is False


def test_find_qmk_userspace(temp_directory):
    (temp_directory / 'qmk.json').write_text('{"userspace_version": 2}')
    os.chdir(temp_directory)

    assert qmk_cli.helpers.find_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_find_qmk_userspace_env(temp_directory):
    with patch.dict('os.environ', {'QMK_USERSPACE': temp_directory.as_posix()}, clear=True):
        assert qmk_cli.helpers.find_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_find_qmk_userspace_env_missing(temp_directory):
    with patch.dict('os.environ', {'QMK_USERSPACE': (temp_directory / 'asdf').as_posix()}, clear=True):
        assert qmk_cli.helpers.find_qmk_userspace().as_posix() == (temp_directory / 'asdf').as_posix()


def test_find_qmk_userspace_config(temp_directory):
    with patch.object(qmk_cli.helpers, 'cli') as cli:
        type(cli.config.user).overlay_dir = PropertyMock(return_value=temp_directory.as_posix())

        assert qmk_cli.helpers.find_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_find_qmk_userspace_config_user():
    with patch.object(qmk_cli.helpers, 'cli') as cli:
        type(cli.config.user).overlay_dir = PropertyMock(return_value='~/asdf')

        assert qmk_cli.helpers.find_qmk_userspace().as_posix() == (Path.home() / 'asdf').as_posix()


def test_find_qmk_userspace_default(temp_directory):
    with patch('pathlib.Path.home') as home:
        home.return_value = temp_directory

        assert qmk_cli.helpers.find_qmk_userspace().as_posix() == (temp_directory / 'qmk_userspace').as_posix()


def test_in_qmk_userspace(temp_directory):
    (temp_directory / 'qmk.json').write_text('{"userspace_version": 2}')
    os.chdir(temp_directory)

    assert qmk_cli.helpers.in_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_in_qmk_userspace_sub(temp_directory):
    (temp_directory / 'qmk.json').write_text('{"userspace_version": 2}')
    (temp_directory / 'keymaps' / 'test').mkdir(parents=True)
    os.chdir(temp_directory / 'keymaps')

    assert qmk_cli.helpers.in_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_in_qmk_userspace_sub_sub(temp_directory):
    (temp_directory / 'qmk.json').write_text('{"userspace_version": 2}')
    (temp_directory / 'keymaps' / 'test').mkdir(parents=True)
    os.chdir(temp_directory / 'keymaps' / 'test')

    assert qmk_cli.helpers.in_qmk_userspace().as_posix() == temp_directory.as_posix()


def test_in_qmk_userspace_invalid(temp_directory):
    os.chdir(temp_directory)

    assert qmk_cli.helpers.in_qmk_userspace() is None
