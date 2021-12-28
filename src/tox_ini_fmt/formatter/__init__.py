from __future__ import annotations

from configparser import ConfigParser
from io import StringIO
from pathlib import Path

from tox_ini_fmt.cli import ToxIniFmtNamespace

from .section_order import order_sections
from .test_env import format_test_env
from .tox_section import format_tox_section

INDENTATION = "    "


def format_tox_ini(tox_ini: Path, opts: ToxIniFmtNamespace | None = None) -> str:
    if opts is None:
        opts = ToxIniFmtNamespace(pin_toxenvs=[])
    parser = ConfigParser(interpolation=None)
    with tox_ini.open("rt"):
        parser.read([tox_ini])

    order_sections(parser, opts.pin_toxenvs)
    format_tox_section(parser, opts.pin_toxenvs)
    for section_name in parser.sections():
        if section_name == "testenv" or section_name.startswith("testenv:"):
            format_test_env(parser, section_name)

    return _generate_tox_ini(parser)


def _generate_tox_ini(parser: ConfigParser) -> str:
    output = StringIO()
    parser.write(output)
    result = output.getvalue().strip() + "\n"
    result = result.replace("\t", INDENTATION)
    result = result.replace(" \n", "\n")
    return result
