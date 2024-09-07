from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_version() -> None:
    import tox_ini_fmt  # noqa: PLC0415

    assert tox_ini_fmt.__version__


def test_help_invocation_as_module() -> None:
    subprocess.check_call([sys.executable, "-m", "tox_ini_fmt", "--help"])


def test_help_invocation_as_script() -> None:
    subprocess.check_call([str(Path(sys.executable).parent / "tox-ini-fmt"), "--help"])
