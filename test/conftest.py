import tempfile
import pytest
from pathlib import Path
from unittest.mock import create_autospec, PropertyMock, MagicMock

from milc import MILCInterface
from milc.configuration import Configuration


def pytest_addoption(parser):
    parser.addoption(
        '--qmk',
        action='store',
        default='wrapper',
        help='options: ./qmk wrapper or real qmk from path',
        choices=('wrapper', 'real'),
    )


@pytest.fixture
def temp_directory():
    """Similar behavior to the default tmpdir fixture except the folder is cleaned up."""
    with tempfile.TemporaryDirectory() as tmp_path:
        yield Path(tmp_path)


@pytest.fixture
def mock_cli():
    """Mock cli to pass to cli subcommands,"""
    ret = create_autospec(MILCInterface)

    # default behavior
    type(ret).config = Configuration()
    ret.config.general.unicode = True
    ret.config.general.color = True
    type(ret).write_config_option = MagicMock()
    type(ret.args).var = PropertyMock(return_value=None)

    return ret
