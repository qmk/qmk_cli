"""Tests for qmk_cli.helpers userspace detection."""
from pathlib import Path

from qmk_cli.helpers import is_qmk_userspace


def test_non_utf8_qmk_json_is_not_a_userspace(tmp_path):
    """A qmk.json that is not decodable as UTF-8 must not crash detection."""
    qmk_json = Path(tmp_path) / 'qmk.json'
    qmk_json.write_bytes(b'{\xff\xfe not valid utf-8')
    assert is_qmk_userspace(Path(tmp_path)) is False


def test_valid_userspace_detected(tmp_path):
    qmk_json = Path(tmp_path) / 'qmk.json'
    qmk_json.write_text('{"userspace_version": "1.0"}', encoding='UTF-8')
    assert is_qmk_userspace(Path(tmp_path)) is True


def test_missing_qmk_json_is_not_a_userspace(tmp_path):
    assert is_qmk_userspace(Path(tmp_path)) is False
