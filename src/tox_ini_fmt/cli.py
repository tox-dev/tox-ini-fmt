"""CLI argument parsing."""

from __future__ import annotations

import os
from argparse import Action, ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import Any, Sequence


class ToxIniFmtNamespace(Namespace):
    """Options for tox-ini-fmt tool."""

    tox_ini: list[Path]
    stdout: bool
    pin_toxenvs: list[str]


def tox_ini_path_creator(argument: str) -> Path:
    """
    Validate that tox.ini can be formatted.

    :param argument: the string argument passed in
    :return: the tox.ini path
    """
    path = Path(argument).absolute()
    if not path.exists():
        msg = "path does not exists"
        raise ArgumentTypeError(msg)
    if not path.is_file():
        msg = "path is not a file"
        raise ArgumentTypeError(msg)
    if not os.access(path, os.R_OK):
        msg = "cannot read path"
        raise ArgumentTypeError(msg)  # pragma: no cover
    if not os.access(path, os.W_OK):
        msg = "cannot write path"
        raise ArgumentTypeError(msg)  # pragma: no cover
    return path


def cli_args(args: Sequence[str]) -> ToxIniFmtNamespace:
    """
    Load the tools options.

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
            parser: ArgumentParser,  # noqa: ARG002
            namespace: Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,  # noqa: ARG002
        ) -> None:
            if isinstance(values, str):  # pragma: no cover
                setattr(namespace, self.dest, [i.strip() for i in values.split(",")])

    parser.add_argument(
        "-p",
        dest="pin_toxenvs",
        metavar="toxenv",
        action=CommaSeparatedStr,
        default=[],
        help="tox environments that pin to the start of the envlist (comma separated)",
    )
    parser.add_argument("tox_ini", nargs="+", type=tox_ini_path_creator, help="tox ini files to format")
    ns = ToxIniFmtNamespace()
    parser.parse_args(namespace=ns, args=args)
    return ns
