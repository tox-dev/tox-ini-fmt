import os
from argparse import Action, ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from typing import Any, List, Optional, Sequence, Union


class ToxIniFmtNamespace(Namespace):
    """Options for tox-ini-fmt tool"""

    tox_ini: Path
    stdout: bool
    pin_toxenvs: List[str]


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
        "-s",
        "--stdout",
        action="store_true",
        help="print the formatted text to the stdout (instead of update in-place)",
    )

    class ComaSeparatedStr(Action):
        def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            values: Union[str, Sequence[Any], None],
            option_string: Optional[str] = None,
        ) -> None:
            if isinstance(values, str):  # pragma: no cover
                setattr(namespace, self.dest, list(i.strip() for i in values.split(",")))

    parser.add_argument(
        "-p",
        dest="pin_toxenvs",
        metavar="toxenv",
        action=ComaSeparatedStr,
        default=[],
        help="tox environments that pin to the start of the envlist (comma separated)",
    )
    parser.add_argument("tox_ini", type=tox_ini_path_creator, help="tox ini file to format")
    return parser.parse_args(namespace=ToxIniFmtNamespace(), args=args)
