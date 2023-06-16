from __future__ import annotations

from typing import TYPE_CHECKING

from tox_ini_fmt.formatter import format_tox_ini

if TYPE_CHECKING:
    from pathlib import Path


def test_upgrade_tox_section(tox_ini: Path) -> None:
    tox_ini.write_text("[tox]\nenvlist =\n test")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    test\n"
