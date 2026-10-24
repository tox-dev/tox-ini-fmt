# tox-ini-fmt

See the [changelog](CHANGELOG.md) for released changes. A user-facing pull request needs a
`changelog.d/+short-name.<category>.md` fragment. The release workflow replaces the name with the squash-merged pull
request number and credits its human authors. Use the `skip news` label for maintenance changes; bot updates need a
fragment only when the pull request supplies one.

Choose `feature` for added or removed Python support and new capabilities, `change` for changed behavior, `bugfix` for
fixes, and `doc` for user documentation. The other categories are `breaking`, `security`, `performance`, `deprecation`,
`removal`, and `packaging`. Keep each fragment about one user-visible change.

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
    rev: 1.10.0
    hooks:
      - id: tox-ini-fmt
        args: [-p, 'fix_lint,type']
```

## cli

Consult the help for the latest usage:

```console
$ tox-ini-fmt --help
usage: tox-ini-fmt [-h] [-s | --check] [-p toxenv] tox_ini [tox_ini ...]

positional arguments:
  tox_ini       tox ini files to format

options:
  -h, --help    show this help message and exit
  -s, --stdout  print the formatted text to the stdout (instead of update in-place)
  --check       check files are formatted without writing them back (exit code 1 on change)
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
1. `testenv`
1. `testenv:*` - `py`/`pypy` envs are ordered in decreasing order by python version, then apply the order defined within
   `envlist` part of `tox` section, you can pin tox elements to the start by using the `-p` flag
1. any other section defined within the file

### `tox` section

Order by:

1. `envlist` - multi-line, start with `py` envs in decreasing python order, then same with `pypy`, then everything else
1. `isolated_build` - `boolean` field
1. `skipsdist` - `boolean` field
1. `skip_missing_interpreters` - `boolean` field
1. `minversion`

### `testenv` section

Order by:

1. `description`
1. `passenv` - multi-line, one environment name to pass per line, sorted by name
1. `setenv` - multi-line, one environment name-value to set per line in format of `key=value`, sorted by key+value
1. `basepython`
1. `skip_install` - `boolean` field
1. `usedevelop` - `boolean` field
1. `deps` - multi-line, order by package name (but keep dependencies with package names separate at end), normalize
   format to remove extra spaces
1. `extras` - multi-line, one extra env per line
1. `parallel_show_output` - `boolean` field
1. `commands` - one command per line, commands that wrap over multiple lines are indented with line two or later by
   extra four spaces
