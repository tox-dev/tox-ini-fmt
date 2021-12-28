from __future__ import annotations

import pytest


@pytest.fixture()
def tox_ini(tmp_path):
    return tmp_path / "tox.ini"
