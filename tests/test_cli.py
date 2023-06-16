from __future__ import annotations

import sys
from stat import S_IREAD, S_IWRITE
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.cli import cli_args

if TYPE_CHECKING:
    from pathlib import Path


def test_cli_tox_ini_ok(tmp_path: Path) -> None:
    path = tmp_path / "tox.ini"
    path.write_text("")
    result = cli_args([str(path)])
    assert result.tox_ini[0] == path


def test_cli_multiple_tox_ini_files_ok(tmp_path: Path) -> None:
    path = tmp_path / "tox.ini"
    path.write_text("")
    path_2 = tmp_path / "tox2.ini"
    path_2.write_text("")
    result = cli_args([str(path), str(path_2)])
    assert result.tox_ini[0] == path
    assert result.tox_ini[1] == path_2


def test_cli_tox_ini_not_exists(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as context:
        cli_args([str(tmp_path / "tox.ini")])
    assert context.value.code != 0
    out, err = capsys.readouterr()
    assert not out
    assert "argument tox_ini: path does not exists" in err


def test_cli_tox_ini_not_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as context:
        cli_args([str(tmp_path)])
    assert context.value.code != 0
    out, err = capsys.readouterr()
    assert not out
    assert "argument tox_ini: path is not a file" in err


@pytest.mark.parametrize(
    ("flag", "error"),
    [
        (S_IREAD, "write"),
        pytest.param(
            S_IWRITE,
            "read",
            marks=pytest.mark.skipif(sys.platform == "win32", reason="On Windows, files cannot be write-only"),
        ),
    ],
)
def test_cli_tox_ini_permission_fail(tmp_path: Path, capsys: pytest.CaptureFixture[str], flag: int, error: str) -> None:
    path = tmp_path / "tox.ini"
    path.write_text("")
    path.chmod(flag)
    try:
        with pytest.raises(SystemExit) as context:
            cli_args([str(path)])
    finally:
        path.chmod(S_IWRITE | S_IREAD)
    assert context.value.code != 0
    out, err = capsys.readouterr()
    assert not out
    assert f"argument tox_ini: cannot {error} path" in err


def test_tox_ini_resolved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "tox.ini"
    path.write_text("")
    result = cli_args(["tox.ini"])
    assert result.tox_ini[0] == path
