from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_version():
    import tox_ini_fmt

    assert tox_ini_fmt.__version__


def test_help_invocation_as_module():
    subprocess.check_call([sys.executable, "-m", "tox_ini_fmt", "--help"])


def test_help_invocation_as_script():
    subprocess.check_call([str(Path(sys.executable).parent / "tox-ini-fmt"), "--help"])
