# Changelog

All notable changes to this project will be documented in this file.

<!-- towncrier release notes start -->

## 1.10.0 (2026-10-10)

- Require Python 3.11 and use Python 3.15 by default.

## 1.9.0 (2026-08-14)

- Read and write `tox.ini` as UTF-8 and add a `--check` mode that reports changes without writing.

## 1.8.1 (2026-07-26)

- Preserve URL dependencies instead of treating them as factor conditionals.

## 1.8.0 (2026-07-21)

- Add Python 3.15 to the test matrix and update formatting tools.

## 1.7.2 (2026-07-07)

- Move development tooling to `tox.toml`, dependency groups, and ty; tighten workflow security checks.

## 1.7.1 (2025-12-12)

- Handle `file|` in `set_env`.

## 1.7.0 (2025-10-09)

- End support for Python 3.9.

## 1.6.0 (2025-07-30)

- Add Python 3.14 support and rename obsolete configuration items.

## 1.5.0 (2025-01-21)

- Update dependencies and development tooling.

## 1.4.1 (2024-09-18)

- Improve CI.

## 1.4.0 (2024-09-13)

- Support dotted version environment names when ordering `env_list`.

## 1.3.2 (2024-09-07)

- Fix type checking.

## 1.3.1 (2023-06-16)

- Add Python 3.12 support and switch to trusted publishing.

## 1.3.0 (2023-04-07)

- Update the configuration syntax to tox v4.

## 1.2.0 (2023-04-06)

- Order `depends` entries.

## 1.1.0 (2023-04-05)

- Support conditional markers in configuration lists.

## 1.0.0 (2023-03-30)

- Extend support for additional keys, support tox v4 aliases, and move pass_env/set_env just before commands.
- Use hatchling instead of setuptools.

## 0.6.1 (2023-01-16)

- Preserve existing line endings and fix Windows test coverage.

## 0.6.0 (2023-01-05)

- Support processing multiple `tox.ini` files at once ([#119](https://github.com/tox-dev/tox-ini-fmt/pull/119))
- Fix `tox.ini` formatting when `envlist` ends with a comma ([#41](https://github.com/tox-dev/tox-ini-fmt/issues/41))

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

## 0.2.0 (2020-09-28)

- Fix package configuration.

## 0.1.0 (2020-09-25)

- Add the pre-commit hook and `--stdout` mode.

### Added

- Base version
