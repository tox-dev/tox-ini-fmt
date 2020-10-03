# Changelog

All notable changes to this project will be documented in this file.

## 0.3.0 (2020-10-03)

- Changed indentation to four spaces ([#26](https://github.com/tox-dev/tox-ini-fmt/issues/26))
- Fix `envlist`/`toxenv` ordering not matching description in README
  ([#18](https://github.com/tox-dev/tox-ini-fmt/issues/18))
- Add ability to pin environments to the start of the `envlist` via the `-p` CLI flag (for example pre-commit should
  always run first) ([#19](https://github.com/tox-dev/tox-ini-fmt/issues/19))
- Change indentation to four spaces, instead of two ([#28](https://github.com/tox-dev/tox-ini-fmt/issues/28))
- Strip empty lines in the `deps` elements ([#20](https://github.com/tox-dev/tox-ini-fmt/issues/20))
- Only strip `.0` suffix from versions when the comparator is `==` or `>=`
  ([#30](https://github.com/tox-dev/tox-ini-fmt/issues/30))

### Added

- Base version
