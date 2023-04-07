from __future__ import annotations

import difflib
import sys
from pathlib import Path
from typing import Iterable, Sequence

from tox_ini_fmt.cli import cli_args
from tox_ini_fmt.formatter import format_tox_ini

GREEN = "\u001b[32m"
RED = "\u001b[31m"
RESET = "\u001b[0m"


def color_diff(diff: Iterable[str]) -> Iterable[str]:
    for line in diff:
        if line.startswith("+"):
            yield GREEN + line + RESET
        elif line.startswith("-"):
            yield RED + line + RESET
        else:
            yield line


def run(args: Sequence[str] | None = None) -> int:
    opts = cli_args(sys.argv[1:] if args is None else args)
    changed = False
    for tox_ini in opts.tox_ini:
        with tox_ini.open("rt") as file:
            before = file.read()
            original_newlines = file.newlines
        if isinstance(original_newlines, tuple):
            original_newlines = original_newlines[0]
        formatted = format_tox_ini(before, opts)
        changed |= before != formatted
        if opts.stdout:  # stdout just prints new format to stdout
            print(formatted, end="")
        else:
            if before != formatted:
                with tox_ini.open("wt", newline=original_newlines) as file:
                    file.write(formatted)
            try:
                name = str(tox_ini.relative_to(Path.cwd()))
            except ValueError:
                name = str(tox_ini)
            diff = (
                difflib.unified_diff(before.splitlines(), formatted.splitlines(), fromfile=name, tofile=name)
                if changed
                else []
            )
            if diff:
                diff_text = "\n".join(color_diff(diff))
                print(diff_text)  # print diff on change
            else:
                print(f"no change for {name}")
    # exit with non success on change
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(run())
