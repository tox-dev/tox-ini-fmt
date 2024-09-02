from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def tox_ini(tmp_path: Path) -> Path:
    return tmp_path / "tox.ini"
