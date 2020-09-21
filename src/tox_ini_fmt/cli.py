import os
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import Sequence


class ToxIniFmtNamespace(Namespace):
    """Options for tox-ini-fmt tool"""

    tox_ini: Path
    in_place: bool


def tox_ini_path_creator(argument: str) -> Path:
    """Validate that tox.ini can be formatted.

    :param argument: the string argument passed in
    :return: the tox.ini path
    """
    path = Path(argument).absolute()
    if not path.exists():
        raise ArgumentTypeError("path does not exists")
    if not path.is_file():
        raise ArgumentTypeError("path is not a file")
    if not os.access(path, os.R_OK):
        raise ArgumentTypeError("cannot read path")
    if not os.access(path, os.W_OK):
        raise ArgumentTypeError("cannot write path")
    return path


def cli_args(args: Sequence[str]) -> ToxIniFmtNamespace:
    """Load the tools options.

    :param args: CLI arguments
    :return: the parsed options
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--in-place", action="store_true", help="write the result back to the file (instead of print to stdout)"
    )
    parser.add_argument("tox_ini", type=tox_ini_path_creator, help="tox ini file to format")
    return parser.parse_args(namespace=ToxIniFmtNamespace(), args=args)
