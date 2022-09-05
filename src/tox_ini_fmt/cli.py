from __future__ import annotations

import os
import re
from argparse import Action, ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import Any, Sequence


class ToxIniFmtNamespace(Namespace):
    """Options for tox-ini-fmt tool"""

    tox_ini: Path
    stdout: bool
    pin_toxenvs: list[str]
    line_ending: str


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
        raise ArgumentTypeError("cannot read path")  # pragma: no cover
    if not os.access(path, os.W_OK):
        raise ArgumentTypeError("cannot write path")  # pragma: no cover
    return path


def cli_args(args: Sequence[str]) -> ToxIniFmtNamespace:
    """Load the tools options.

    :param args: CLI arguments
    :return: the parsed options
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="print the formatted text to the stdout (instead of update in-place)",
    )

    class CommaSeparatedStr(Action):
        def __call__(
            self,
            parser: ArgumentParser,  # noqa: U100
            namespace: Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,  # noqa: U100
        ) -> None:
            if isinstance(values, str):  # pragma: no cover
                setattr(namespace, self.dest, [i.strip() for i in values.split(",")])

    class LineEndingChecker(Action):
        def __call__(
            self,
            parser: ArgumentParser,  # noqa: U100
            namespace: Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,  # noqa: U100
        ) -> None:
            if isinstance(values, str):  # pragma: no cover
                if re.match(r"^(auto|lf|crlf|cr|system)$", values):
                    setattr(namespace, self.dest, values)
                else:
                    raise ValueError(f"{values} is not a valid line separator")

    parser.add_argument(
        "-p",
        dest="pin_toxenvs",
        metavar="toxenv",
        action=CommaSeparatedStr,
        default=[],
        help="tox environments that pin to the start of the envlist (comma separated)",
    )
    parser.add_argument(
        "-l",
        dest="line_ending",
        metavar="line_ending",
        action=LineEndingChecker,
        default="auto",
        help="force the line ending in tox.ini (auto, lf, crlf, cr, system)",
    )
    parser.add_argument("tox_ini", type=tox_ini_path_creator, help="tox ini file to format")
    return parser.parse_args(namespace=ToxIniFmtNamespace(), args=args)
