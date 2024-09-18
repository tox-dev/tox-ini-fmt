# tox-ini-fmt

[![PyPI](https://img.shields.io/pypi/v/tox-ini-fmt?style=flat-square)](https://pypi.org/project/tox-ini-fmt)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/tox-ini-fmt?style=flat-square)](https://pypi.org/project/tox-ini-fmt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tox-ini-fmt?style=flat-square)](https://pypi.org/project/tox-ini-fmt)
[![Downloads](https://static.pepy.tech/badge/tox-ini-fmt/month)](https://pepy.tech/project/tox-ini-fmt)
[![PyPI - License](https://img.shields.io/pypi/l/tox-ini-fmt?style=flat-square)](https://opensource.org/licenses/MIT)
[![check](https://github.com/tox-dev/tox-ini-fmt/actions/workflows/check.yaml/badge.svg)](https://github.com/tox-dev/tox-ini-fmt/actions/workflows/check.yaml)

apply a consistent format to `tox.ini` files

## installation

`pip install tox-ini-fmt`

## as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/tox-dev/tox-ini-fmt
  rev: "1.3.1"
  hooks:
    - id: tox-ini-fmt
      args: ["-p", "fix_lint,type"]
```

## cli

Consult the help for the latest usage:

```console
$ tox-ini-fmt --help
usage: tox-ini-fmt [-h] [-s] [-p toxenv] tox_ini

positional arguments:
  tox_ini       tox ini file to format

optional arguments:
  -h, --help    show this help message and exit
  -s, --stdout  print the formatted text to the stdout (instead of update in-place)
  -p toxenv     tox environments that pin to the start of the envlist (comma separated)
```

## what does it do?

### It does not

- Format any other section beside `tox`/`testenv:*` (other than put this sections to the end of the file)

### General

- `boolean` fields are normalized to `true` or `false`
- all fields are stripped of white space on both end
- values that contain a list are split one value per line (PR/merge friendly)
- indent multi-line values by four spaces, and start on new line
- substitutions within multi-line (excluding `commands`) are moved to the start of the list (order kept)

### Ordering of sections

Applies the following section order:

1. `tox`
2. `testenv`
3. `testenv:*` - `py`/`pypy` envs are ordered in decreasing order by python version, then apply the order defined within
   `envlist` part of `tox` section, you can pin tox elements to the start by using the `-p` flag
4. any other section defined within the file

### `tox` section

Order by:

1. `envlist` - multi-line, start with `py` envs in decreasing python order, then same with `pypy`, then everything else
2. `isolated_build` - `boolean` field
3. `skipsdist` - `boolean` field
4. `skip_missing_interpreters` - `boolean` field
5. `minversion`

### `testenv` section

Order by:

1. `description`
2. `passenv` - multi-line, one environment name to pass per line, sorted by name
3. `setenv` - multi-line, one environment name-value to set per line in format of `key=value`, sorted by key+value
4. `basepython`
5. `skip_install` - `boolean` field
6. `usedevelop` - `boolean` field
7. `deps` - multi-line, order by package name (but keep dependencies with package names separate at end), normalize
   format to remove extra spaces
8. `extras` - multi-line, one extra env per line
9. `parallel_show_output` - `boolean` field
10. `commands` - one command per line, commands that wrap over multiple lines are indented with line two or later by
    extra four spaces
