import sys
from typing import Optional, Sequence

from tox_ini_fmt.cli import cli_args
from tox_ini_fmt.formatter import format_tox_ini


def run(args: Optional[Sequence[str]] = None) -> int:
    opts = cli_args(sys.argv[1:] if args is None else args)
    formatted = format_tox_ini(opts.tox_ini)
    if opts.in_place:
        opts.tox_ini.write_text(formatted)
        print(f"updated {opts.tox_ini}")
    else:
        print(formatted, end="")
    return 0


if __name__ == "__main__":
    sys.exit(run())
