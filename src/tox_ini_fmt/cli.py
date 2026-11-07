"""CLI argument parsing."""

from __future__ import annotations

import os
from argparse import Action, ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence


def cli_args(args: Sequence[str]) -> ToxIniFmtNamespace:
    """
    Load the tools options.

    :param args: CLI arguments
    :returns: the parsed options
    """
    parser = ArgumentParser()
    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="print the formatted text to the stdout (instead of update in-place)",
    )
    output_mode.add_argument(
        "--check",
        action="store_true",
        help="check files are formatted without writing them back (exit code 1 on change)",
    )

    class CommaSeparatedStr(Action):
        def __call__(
            self,
            parser: ArgumentParser,  # ruff:ignore[unused-method-argument] # argparse fixes this signature
            namespace: Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,  # ruff:ignore[unused-method-argument] # argparse fixes this signature
        ) -> None:
            if isinstance(values, str):  # pragma: no cover # argparse always passes a string
                setattr(namespace, self.dest, [i.strip() for i in values.split(",")])

    parser.add_argument(
        "-p",
        dest="pin_toxenvs",
        metavar="toxenv",
        action=CommaSeparatedStr,
        default=[],
        help="tox environments that pin to the start of the envlist (comma separated)",
    )
    parser.add_argument("tox_ini", nargs="+", type=_tox_ini_path_creator, help="tox ini files to format")
    ns = ToxIniFmtNamespace()
    parser.parse_args(namespace=ns, args=args)
    return ns


def _tox_ini_path_creator(argument: str) -> Path:
    # Validate that tox.ini can be formatted.
    #
    # :param argument: the string argument passed in
    # :returns: the tox.ini path
    # :raises ArgumentTypeError:
    path = Path(argument).absolute()
    if not path.exists():
        msg = "path does not exists"
        raise ArgumentTypeError(msg)
    if not path.is_file():
        msg = "path is not a file"
        raise ArgumentTypeError(msg)
    if not os.access(path, os.R_OK):
        msg = "cannot read path"
        raise ArgumentTypeError(msg)  # pragma: no cover # the write-only test is skipped on Windows
    if not os.access(path, os.W_OK):
        msg = "cannot write path"
        raise ArgumentTypeError(msg)
    return path


class ToxIniFmtNamespace(Namespace):
    """
    Options for tox-ini-fmt tool.

    :ivar tox_ini: the tox ini files to format
    :ivar stdout: print the formatted text instead of updating the files in place
    :ivar check: report the files that need formatting, without writing them back
    :ivar pin_toxenvs: tox environments to move to the start of the env list
    """

    tox_ini: list[Path]
    stdout: bool
    check: bool
    pin_toxenvs: list[str]


__all__ = [
    "ToxIniFmtNamespace",
    "cli_args",
]
