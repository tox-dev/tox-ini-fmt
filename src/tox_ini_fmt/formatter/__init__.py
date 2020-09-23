from configparser import ConfigParser
from io import StringIO
from pathlib import Path

from .section_order import order_sections
from .test_env import format_test_env
from .tox_section import format_tox_section


def format_tox_ini(tox_ini: Path) -> str:
    parser = ConfigParser()
    with tox_ini.open("rt"):
        parser.read([tox_ini])

    order_sections(parser)
    format_tox_section(parser)

    for section_name in parser.sections():
        if section_name == "testenv" or section_name.startswith("testenv:"):
            format_test_env(parser, section_name)

    return _generate_tox_ini(parser)


def _generate_tox_ini(parser: ConfigParser) -> str:
    output = StringIO()
    parser.write(output)
    result = output.getvalue().strip() + "\n"
    result = result.replace("\t", "  ")
    result = result.replace(" \n", "\n")
    return result
