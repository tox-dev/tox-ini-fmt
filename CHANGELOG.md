# Changelog

All notable changes to this project will be documented in this file.

<!-- towncrier release notes start -->

<a name="release-1-10-0"></a>

## 1.10.0 (2026-10-10)

<a name="release-1-10-0-added"></a>

### Added

- End support for Python 3.10 ([#377](https://github.com/tox-dev/tox-ini-fmt/pull/377)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-10-0-changes"></a>

### Changes

- Use Python 3.15 by default ([#377](https://github.com/tox-dev/tox-ini-fmt/pull/377)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-9-0"></a>

## 1.9.0 (2026-08-14)

<a name="release-1-9-0-added"></a>

### Added

- Report formatting changes without writing with `--check` ([#361](https://github.com/tox-dev/tox-ini-fmt/pull/361)) by
  [@dchaudhari7177](https://github.com/dchaudhari7177).

<a name="release-1-9-0-fixed"></a>

### Fixed

- Read and write `tox.ini` as UTF-8 ([#362](https://github.com/tox-dev/tox-ini-fmt/pull/362)) by
  [@aroh3006](https://github.com/aroh3006).

<a name="release-1-8-1"></a>

## 1.8.1 (2026-07-26)

<a name="release-1-8-1-fixed"></a>

### Fixed

- Preserve URL dependencies instead of treating them as factor conditionals
  ([#353](https://github.com/tox-dev/tox-ini-fmt/pull/353)) by [@dchaudhari7177](https://github.com/dchaudhari7177).

<a name="release-1-8-0"></a>

## 1.8.0 (2026-07-21)

<a name="release-1-8-0-added"></a>

### Added

- Support Python 3.15 ([#350](https://github.com/tox-dev/tox-ini-fmt/pull/350)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-7-2"></a>

## 1.7.2 (2026-07-07)

<a name="release-1-7-1"></a>

## 1.7.1 (2025-12-12)

<a name="release-1-7-1-fixed"></a>

### Fixed

- Handle `file|` in `set_env` ([#296](https://github.com/tox-dev/tox-ini-fmt/pull/296)) by
  [@daniel-k](https://github.com/daniel-k).

<a name="release-1-7-0"></a>

## 1.7.0 (2025-10-09)

<a name="release-1-7-0-added"></a>

### Added

- End support for Python 3.9 ([#284](https://github.com/tox-dev/tox-ini-fmt/pull/284)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-6-0"></a>

## 1.6.0 (2025-07-30)

<a name="release-1-6-0-added"></a>

### Added

- Support Python 3.14 ([#264](https://github.com/tox-dev/tox-ini-fmt/pull/264)) by
  [@ssbarnea](https://github.com/ssbarnea).

<a name="release-1-6-0-changes"></a>

### Changes

- Rename obsolete tox configuration keys when formatting ([#263](https://github.com/tox-dev/tox-ini-fmt/pull/263)) by
  [@ssbarnea](https://github.com/ssbarnea).

<a name="release-1-5-0"></a>

## 1.5.0 (2025-01-21)

<a name="release-1-4-1"></a>

## 1.4.1 (2024-09-18)

<a name="release-1-4-0"></a>

## 1.4.0 (2024-09-13)

<a name="release-1-4-0-fixed"></a>

### Fixed

- Order environment names containing dotted versions in `env_list`
  ([#218](https://github.com/tox-dev/tox-ini-fmt/pull/218)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-3-2"></a>

## 1.3.2 (2024-09-07)

<a name="release-1-3-2-added"></a>

### Added

- Support Python 3.13 by [@gaborbernat](https://github.com/gaborbernat).
- End support for Python 3.7 by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-3-1"></a>

## 1.3.1 (2023-06-16)

<a name="release-1-3-1-added"></a>

### Added

- Support Python 3.12 ([#152](https://github.com/tox-dev/tox-ini-fmt/pull/152)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-3-0"></a>

## 1.3.0 (2023-04-07)

<a name="release-1-3-0-changes"></a>

### Changes

- Rename obsolete tox configuration keys to tox v4 syntax ([#146](https://github.com/tox-dev/tox-ini-fmt/pull/146)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-2-0"></a>

## 1.2.0 (2023-04-06)

<a name="release-1-2-0-changes"></a>

### Changes

- Order `depends` entries ([#143](https://github.com/tox-dev/tox-ini-fmt/pull/143)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-1-0"></a>

## 1.1.0 (2023-04-05)

<a name="release-1-1-0-added"></a>

### Added

- Format conditional markers in configuration lists ([#141](https://github.com/tox-dev/tox-ini-fmt/pull/141)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-1-0-0"></a>

## 1.0.0 (2023-03-30)

<a name="release-1-0-0-added"></a>

### Added

- Format additional tox v4 configuration keys and aliases ([#137](https://github.com/tox-dev/tox-ini-fmt/pull/137)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-6-1"></a>

## 0.6.1 (2023-01-16)

<a name="release-0-6-1-fixed"></a>

### Fixed

- Preserve existing line endings ([#122](https://github.com/tox-dev/tox-ini-fmt/pull/122)) by
  [@kurtmckee](https://github.com/kurtmckee).

<a name="release-0-6-0"></a>

## 0.6.0 (2023-01-05)

<a name="release-0-6-0-added"></a>

### Added

- Format multiple `tox.ini` files in one invocation ([#119](https://github.com/tox-dev/tox-ini-fmt/pull/119)) by
  [@pdecat](https://github.com/pdecat).

<a name="release-0-5-2"></a>

## 0.5.2 (2021-12-28)

<a name="release-0-5-2-added"></a>

### Added

- End support for Python 3.6 by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-5-1"></a>

## 0.5.1 (2021-06-25)

<a name="release-0-5-1-added"></a>

### Added

- Support Python 3.9 ([#45](https://github.com/tox-dev/tox-ini-fmt/pull/45)) by [@hugovk](https://github.com/hugovk).

<a name="release-0-5-1-fixed"></a>

### Fixed

- Preserve configuration values without ConfigParser interpolation
  ([#66](https://github.com/tox-dev/tox-ini-fmt/pull/66)) by [@wwuck](https://github.com/wwuck).

<a name="release-0-5-0"></a>

## 0.5.0 (2020-10-06)

<a name="release-0-5-0-added"></a>

### Added

- Colorize formatter diffs ([#44](https://github.com/tox-dev/tox-ini-fmt/pull/44)) by
  [@hugovk](https://github.com/hugovk).

<a name="release-0-5-0-fixed"></a>

### Fixed

- Format `envlist` when its input ends with a comma ([#43](https://github.com/tox-dev/tox-ini-fmt/pull/43)) by
  [@jugmac00](https://github.com/jugmac00).

<a name="release-0-4-0"></a>

## 0.4.0 (2020-10-04)

<a name="release-0-4-0-added"></a>

### Added

- Format `-r` requirements and conditional markers in `deps` ([#39](https://github.com/tox-dev/tox-ini-fmt/pull/39)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-4-0-changes"></a>

### Changes

- Move multiline substitutions before other values while preserving their order
  ([#38](https://github.com/tox-dev/tox-ini-fmt/pull/38)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-4-0-fixed"></a>

### Fixed

- Preserve substitutions in `deps` and `setenv` ([#39](https://github.com/tox-dev/tox-ini-fmt/pull/39)) by
  [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-3-0"></a>

## 0.3.0 (2020-10-03)

<a name="release-0-3-0-added"></a>

### Added

- Pin selected environments to the start of `envlist` with `-p` ([#31](https://github.com/tox-dev/tox-ini-fmt/pull/31))
  by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-3-0-changes"></a>

### Changes

- Indent formatted configuration with four spaces ([#28](https://github.com/tox-dev/tox-ini-fmt/pull/28)) by
  [@jugmac00](https://github.com/jugmac00).

<a name="release-0-3-0-fixed"></a>

### Fixed

- Keep `envlist` and `toxenv` ordering consistent with the documented rules
  ([#31](https://github.com/tox-dev/tox-ini-fmt/pull/31)) by [@gaborbernat](https://github.com/gaborbernat).
- Skip empty dependency lines ([#20](https://github.com/tox-dev/tox-ini-fmt/pull/20)) by
  [@Julian](https://github.com/Julian).
- Preserve a `.0` version suffix for compatible-release constraints
  ([#30](https://github.com/tox-dev/tox-ini-fmt/pull/30)) by [@jugmac00](https://github.com/jugmac00).

<a name="release-0-2-0"></a>

## 0.2.0 (2020-09-28)

<a name="release-0-2-0-added"></a>

### Added

- Format test environments, including `setenv`, `passenv`, and `skip_install`
  ([#6](https://github.com/tox-dev/tox-ini-fmt/pull/6)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-2-0-changes"></a>

### Changes

- Print a diff and return a nonzero status when formatting changes a file
  ([#10](https://github.com/tox-dev/tox-ini-fmt/pull/10)) by [@gaborbernat](https://github.com/gaborbernat).

<a name="release-0-1-0"></a>

## 0.1.0 (2020-09-25)

<a name="release-0-1-0-added"></a>

### Added

- Format `tox.ini` sections and environment lists ([#1](https://github.com/tox-dev/tox-ini-fmt/pull/1)) by
  [@gaborbernat](https://github.com/gaborbernat).
- Run the formatter as a pre-commit hook or print its output with `--stdout`
  ([#9](https://github.com/tox-dev/tox-ini-fmt/pull/9)) by [@gaborbernat](https://github.com/gaborbernat).
