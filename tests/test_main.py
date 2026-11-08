from __future__ import annotations

import difflib
import subprocess
import sys
from typing import TYPE_CHECKING, Final

import pytest

from tox_ini_fmt.__main__ import GREEN, RED, RESET, color_diff, run

if TYPE_CHECKING:
    from pathlib import Path


def test_color_diff() -> None:
    before = """
    abc
    def
    ghi
"""
    after = """
    abc
    abc
    def
"""
    diff = difflib.unified_diff(before.splitlines(), after.splitlines())
    expected_lines = f"""
{RED}---
{RESET}
{GREEN}+++
{RESET}
@@ -1,4 +1,4 @@


     abc
{GREEN}+    abc{RESET}
     def
{RED}-    ghi{RESET}
""".strip().splitlines()

    diff_color = color_diff(diff)

    output_lines = [line.rstrip() for line in "\n".join(diff_color).splitlines()]
    assert output_lines == expected_lines


@pytest.mark.parametrize(
    ("start", "outcome", "code", "output"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            1,
            "--- tox.ini\n\n+++ tox.ini\n\n@@ -1,4 +1,6 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n-env_list=py311,py310\n+env_list =\n+    py311\n+    py310\n",
            id="change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            0,
            "no change for tox.ini\n",
            id="no-change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n[testenv]\ncommands=pytest --log-format='%(asctime)s'",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            1,
            "--- tox.ini\n\n+++ tox.ini\n\n@@ -1,5 +1,7 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n+\n [testenv]\n-commands=pytest --log-format='%(asctime)s'\n"
            "+commands =\n+    pytest --log-format='%(asctime)s'\n",
            id="change-testenv",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            0,
            "no change for tox.ini\n",
            id="no-change-testenv",
        ),
    ],
)
def test_main(  # ruff:ignore[too-many-arguments] # fixtures and parametrized cases add arguments
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    start: str,
    outcome: str,
    code: int,
    output: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)

    assert run([str(tox_ini)]) == code

    out, err = capsys.readouterr()
    assert not err
    assert tox_ini.read_text() == outcome
    assert out.replace(GREEN, "").replace(RED, "").replace(RESET, "") == output


@pytest.mark.parametrize(
    ("start", "outcome", "code"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            1,
            id="change",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            0,
            id="no-change",
        ),
    ],
)
def test_main_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    start: str,
    outcome: str,
    code: int,
) -> None:
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)

    assert run([str(tox_ini), "--stdout"]) == code

    out, err = capsys.readouterr()
    assert not err
    assert out == outcome


def test_main_names_file_outside_cwd(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text("[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310")

    assert run([str(tox_ini), "--check"]) == 1

    out, _ = capsys.readouterr()
    assert f"--- {tox_ini}\n" in out.replace(RED, "").replace(RESET, "")


_NON_ASCII: Final[str] = (
    "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n\n[testenv]\ncommands =\n    pytest -k 丁\n"
)


def test_non_ascii_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(_NON_ASCII, encoding="utf-8")

    assert run([str(tox_ini)]) == 0

    capsys.readouterr()
    assert tox_ini.read_text(encoding="utf-8") == _NON_ASCII


def test_non_ascii_ignores_locale_encoding(tmp_path: Path) -> None:
    # -X warn_default_encoding turns any locale-dependent open() into an EncodingWarning, so this fails on
    # every platform rather than only where the locale encoding cannot represent the file.
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(_NON_ASCII, encoding="utf-8")

    subprocess.check_call([
        sys.executable,
        "-X",
        "warn_default_encoding",
        "-W",
        "error::EncodingWarning",
        "-m",
        "tox_ini_fmt",
        str(tox_ini),
    ])


@pytest.mark.parametrize(
    ("start", "code", "output"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            1,
            "--- tox.ini\n\n+++ tox.ini\n\n@@ -1,4 +1,6 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n-env_list=py311,py310\n+env_list =\n+    py311\n+    py310\n",
            id="change",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            0,
            "no change for tox.ini\n",
            id="no-change",
        ),
    ],
)
def test_main_check(  # ruff:ignore[too-many-arguments] # fixtures and parametrized cases add arguments
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    start: str,
    code: int,
    output: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)

    assert run([str(tox_ini), "--check"]) == code

    assert tox_ini.read_text() == start
    out, err = capsys.readouterr()
    assert not err
    assert out.replace(GREEN, "").replace(RED, "").replace(RESET, "") == output


def test_main_reports_unchanged_file_after_changed_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    changed = tmp_path / "first.ini"
    changed.write_text("[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310")
    unchanged = tmp_path / "second.ini"
    unchanged.write_text("[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n")

    assert run([str(changed), str(unchanged)]) == 1

    out, err = capsys.readouterr()
    assert not err
    assert out.endswith("no change for second.ini\n")
