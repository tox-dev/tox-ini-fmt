from __future__ import annotations

import difflib
from pathlib import Path

import pytest

import tox_ini_fmt.__main__
from tox_ini_fmt.__main__ import GREEN, RED, RESET, color_diff, run


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
        (
            "[tox]\nenvlist=py39,py38",
            "[tox]\nenvlist =\n    py39\n    py38\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,2 +1,4 @@\n\n "
            "[tox]\n-envlist=py39,py38\n+envlist =\n+    py39\n+    py38\n",
        ),
        ("[tox]\nenvlist =\n    py39\n    py38\n", "[tox]\nenvlist =\n    py39\n    py38\n", "no change for {0}\n"),
        (
            "[testenv]\ncommands=pytest --log-format='%(asctime)s'",
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,2 +1,3 @@\n\n "
            "[testenv]\n-commands=pytest --log-format='%(asctime)s'\n"
            "+commands =\n+    pytest --log-format='%(asctime)s'\n",
        ),
        (
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "no change for {0}\n",
        ),
    ],
)
def test_main(
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
