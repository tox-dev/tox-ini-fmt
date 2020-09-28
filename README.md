# tox-ini-fmt

![check](https://github.com/tox-dev/tox-ini-fmt/workflows/check/badge.svg?branch=main)

# setup-cfg-fmt

apply a consistent format to `tox.ini` files

## installation

`pip install tox-ini-fmt`

## as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/tox-dev/tox-ini-fmt
  rev: v0.0.1
  hooks:
    - id: tox-ini-fmt
```

## cli

Consult the help for the latest usage:

````console
$ tox-ini-fmt --help
usage: tox-ini-fmt [-h] [-s] tox_ini

positional arguments:
  tox_ini       tox ini file to format

optional arguments:
  -h, --help    show this help message and exit
  -s, --stdout  print the formatted text to the stdout (instead of update in-place)```
````

## what does it do?

### General

- `boolean` fields are normalized to `true` or `false`
- are fields are stripped of white space on both end
- values that contain a list are split one value per line (PR/merge friendly)
- indent multi-line values by two space, and start on new line

### Ordering of sections

Applies the following section order:

1. `tox`
2. `testenv`
3. `testenv:*` - `py`/`pypy` envs are ordered in decreasing order by python version, then apply the order defined within
   `envlist` part of `tox` section
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
2. `passenv` - one environment name to pass per line, sorted by name
3. `setenv` - one environment name-value to set per line in format of `key=value`, sorted by key+value
4. `basepython`
5. `skip_install` - `boolean` field
6. `usedevelop` - `boolean` field
7. `deps` - multi-line, order by package name (but keep dependencies with package names separate at end), normalize
   format to remove extra spaces
8. `extras` - multi-line, one extra env per line
9. `parallel_show_output` - `boolean` field
10. `commands` - one command per line, commands that wrap over multiple lines are indented with line two or later by
    extra two space
