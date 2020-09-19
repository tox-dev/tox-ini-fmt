import sys
from typing import Optional, Sequence

from tox_ini_fmt.cli import cli_args
from tox_ini_fmt.formatter import format_tox_ini


def run(args: Optional[Sequence[str]] = None) -> int:
    opts = cli_args(sys.argv[1:] if args is None else args)
    print(format_tox_ini(opts.tox_ini))
    return 0


if __name__ == "__main__":
    sys.exit(run())
