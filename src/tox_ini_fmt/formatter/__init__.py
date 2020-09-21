from configparser import ConfigParser
from io import StringIO
from pathlib import Path

from .section_order import order_sections
from .tox_section import format_tox_section


def format_tox_ini(tox_ini: Path) -> str:
    parser = ConfigParser()
    with tox_ini.open("rt"):
        parser.read([tox_ini])

    format_tox_section(parser)
    order_sections(parser)

    return _generate_tox_ini(parser)


def _generate_tox_ini(parser: ConfigParser) -> str:
    output = StringIO()
    parser.write(output)
    result = output.getvalue().strip() + "\n"
    result = result.replace("\t", "  ")
    result = result.replace(" \n", "\n")
    return result
