# Changelog

All notable changes to this project will be documented in this file.

## 0.6.0 (2023-01-05)

- Support processing multiple `tox.ini` files at once ([#119](https://github.com/tox-dev/tox-ini-fmt/pull/119))
- Fix `tox.ini` formatting when `envlist` ends with a comma
  ([#41](https://github.com/tox-dev/tox-ini-fmt/issues/41))

## 0.5.2 (2021-12-28)

- Drop Python 3.6 support.

## 0.5.1 (2021-06-25)

- Disable config parser interpolation

## 0.5.0 (2020-10-06)

- Diffs are now colored.

## 0.4.0 (2020-10-04)

- Substitutions for multi-line values go now to the beginning of the configuration (to allow overwriting inherited
  values), and in case of multiple such the order is kept ([#22](https://github.com/tox-dev/tox-ini-fmt/issues/22))
- Fixed substitutions not being supported within `deps` and `setenv`
  ([#22](https://github.com/tox-dev/tox-ini-fmt/issues/22))
- Support `-r` and conditional markers within `deps` ([#21](https://github.com/tox-dev/tox-ini-fmt/issues/21))

## 0.3.0 (2020-10-03)

- Changed indentation to four spaces, instead of two ([#26](https://github.com/tox-dev/tox-ini-fmt/issues/26))
- Fix `envlist`/`toxenv` ordering not matching description in README
  ([#18](https://github.com/tox-dev/tox-ini-fmt/issues/18))
- Add ability to pin environments to the start of the `envlist` via the `-p` CLI flag (for example pre-commit should
  always run first) ([#19](https://github.com/tox-dev/tox-ini-fmt/issues/19))
- Strip empty lines in the `deps` elements ([#17](https://github.com/tox-dev/tox-ini-fmt/issues/17))
- Only strip `.0` suffix from versions when the comparator is `==` or `>=`
  ([#30](https://github.com/tox-dev/tox-ini-fmt/issues/30))

### Added

- Base version
