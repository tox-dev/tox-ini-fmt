from __future__ import annotations

import collections
import difflib
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

from tox_ini_fmt.cli import cli_args
from tox_ini_fmt.formatter import format_tox_ini

GREEN = "\u001b[32m"
RED = "\u001b[31m"
RESET = "\u001b[0m"

CRLF = b"\r\n"
LF = b"\n"
CR = b"\r"
# Prefer LF to CRLF to CR, but detect CRLF before LF
ALL_ENDINGS = (CR, CRLF, LF)
FIX_TO_LINE_ENDING = {
    "cr": CR.decode(encoding="ansi"),
    "crlf": CRLF.decode(encoding="ansi"),
    "lf": LF.decode(encoding="ansi"),
}


def color_diff(diff: Iterable[str]) -> Iterable[str]:
    for line in diff:
        if line.startswith("+"):
            yield GREEN + line + RESET
        elif line.startswith("-"):
            yield RED + line + RESET
        else:
            yield line


# partly copied from: https://github.com/pre-commit/pre-commit-hooks/blob/main/pre_commit_hooks/mixed_line_ending.py
def detect_line_ending(filename: str) -> str:
    with open(filename, "rb") as f:
        contents = f.read()

    counts: dict[bytes, int] = collections.defaultdict(int)

    for line in contents.splitlines(True):
        for ending in ALL_ENDINGS:
            if line.endswith(ending):
                counts[ending] += 1
                break

    max_ending: bytes = os.linesep.encode(encoding="ascii")
    max_lines: int = 0
    # ordering is important here such that lf > crlf > cr
    for ending_type in ALL_ENDINGS:
        # also important, using >= to find a max that prefers the last
        if counts[ending_type] >= max_lines:
            max_ending = ending_type
            max_lines = counts[ending_type]
    return max_ending.decode(encoding="ascii")


def run(args: Sequence[str] | None = None) -> int:
    opts = cli_args(sys.argv[1:] if args is None else args)
    formatted = format_tox_ini(opts.tox_ini, opts)
    before = opts.tox_ini.read_text()
    changed = before != formatted
    if opts.stdout:  # stdout just prints new format to stdout
        print(formatted, end="")
    else:
        newline: str | None = None
        if re.match(r"^(lf|crlf|cr)$", opts.line_ending):
            newline = FIX_TO_LINE_ENDING[opts.line_ending]
        elif opts.line_ending == "auto":
            newline = detect_line_ending(str(opts.tox_ini))
        opts.tox_ini.write_text(formatted, newline=newline)
        try:
            name = str(opts.tox_ini.relative_to(Path.cwd()))
        except ValueError:
            name = str(opts.tox_ini)
        diff = (
            difflib.unified_diff(before.splitlines(), formatted.splitlines(), fromfile=name, tofile=name)
            if changed
            else []
        )
        if diff:
            diff = color_diff(diff)
            print("\n".join(diff))  # print diff on change
        else:
            print(f"no change for {name}")
    # exit with non success on change
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(run())
