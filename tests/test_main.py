from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

import pytest

import tox_ini_fmt.__main__
from tox_ini_fmt.__main__ import GREEN, RED, RESET, color_diff, run

if TYPE_CHECKING:
    from pathlib import Path


def test_color_diff() -> None:
    # Arrange
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

    # Act
    diff_color = color_diff(diff)

    # Assert
    output_lines = [line.rstrip() for line in "\n".join(diff_color).splitlines()]
    assert output_lines == expected_lines


def no_color(diff: str) -> str:
    return diff


@pytest.mark.parametrize("in_place", [True, False])
@pytest.mark.parametrize("cwd", [True, False])
@pytest.mark.parametrize(
    ("start", "outcome", "output"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,4 +1,6 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n-env_list=py311,py310\n+env_list =\n+    py311\n+    py310\n",
            id="change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "no change for {0}\n",
            id="no-change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n[testenv]\ncommands=pytest --log-format='%(asctime)s'",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,5 +1,7 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n+\n [testenv]\n-commands=pytest --log-format='%(asctime)s'\n"
            "+commands =\n+    pytest --log-format='%(asctime)s'\n",
            id="change-testenv",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "no change for {0}\n",
            id="no-change-testenv",
        ),
    ],
)
def test_main(  # noqa: PLR0913
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    in_place: bool,
    cwd: bool,
    start: str,
    outcome: str,
    output: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tox_ini_fmt.__main__, "color_diff", no_color)
    if cwd:
        monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)
    args = [str(tox_ini)]
    if not in_place:
        args.append("--stdout")

    result = run(args)
    assert result == (0 if start == outcome else 1)

    out, err = capsys.readouterr()
    assert not err

    if in_place:
        name = "tox.ini" if cwd else str(tmp_path / "tox.ini")
        output = output.format(name)
        assert tox_ini.read_text() == outcome
        assert out == output
    else:
        assert out == outcome
