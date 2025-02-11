# vspect

[![tests](https://github.com/drivendataorg/vspect/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drivendataorg/vspect/actions?query=workflow%3Atests+branch%3Amain)
[![codecov](https://codecov.io/gh/drivendataorg/vspect/branch/main/graph/badge.svg)](https://codecov.io/gh/drivendataorg/vspect)

**vspect** (**v**ersion in**spect**) is a simple and lightweight command-line utility for working with Python package version strings. It was created to make it easier to read and format version strings when doing automated package releases in CI.

There are two main parts to using vspect:

1. **Getting a version string** by using one of the following commands:
    - Use the **`package`** command with a package name, and vspect will look up that package's version in the current virtual environment.
    - Use the **`read`** command to read a statically-defined version from a `pyproject.toml` file. Give it either the file path or its parent directory path.
    - Use the **`parse`** command to with a version string you provide directly.
2. **Render it according to a specified format** by optionally providing a Python formatting string. If not specified, the full version will be printed.

Here are some examples:

```sh
# Look up a package's version
vspect package pip
#> 25.0.1

# Provide a format string to customize the format
vspect package pip "{major_minor_version}"
#> 25.0

# Read from pyproject.toml. Can either be direct path or its parent directory
vspect read . "{major_minor_version}"
#> 0.1

# Parse a directly given version string
vspect parse 1.2.3.post4.dev5 "v{major}.{minor}.{patch}{post}"
#> v1.2.3post4
```

See the ["Format string"](#format-string) section for all available replacement fields.

vspect is lightweight with minimal dependencies. It only depends on the [packaging](https://packaging.pypa.io/en/stable/) package published by the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/) and a [backport](https://github.com/hukkin/tomli) of the standard library's tomllib for older versions of Python.

## Installation

```sh
pip install git+https://github.com/drivendataorg/vspect.git#egg=vspect
```

## Basic usage

```sh
vspect package PACKAGE_NAME [FORMAT_STRING]
# or
vspect read FILE_OR_DIR_PATH [FORMAT_STRING]
# or
vspect parse VERSION [FORMAT_STRING]
```

The `package` subcommand requires that vspect is installed in the same virtual environment as the package you are trying to look up.

## Format string

Both the `package` and `parse` subcommands take an optional `FORMAT_STRING`. The format string is just a regular Python format string that gets passed to `str.format()`. See ["Format String Syntax"](https://docs.python.org/3/library/string.html#formatstrings) in Python's documentation for additional help. The following replacement field names are passed in:

| Replacement field       | Description                                                     | Example                         |
|-------------------------|-----------------------------------------------------------------|---------------------------------|
| `version`              | The full version string.                                       | `1.2.3.post4.dev5`             |
| `base_version`         | Excludes dev, pre, post, and local.                           | `1.2.3.post4.dev5` → `1.2.3`   |
| `major_minor_version`  | The major and minor version string only.                       | `1.2.3` → `1.2`                |
| `public_version`       | Excludes local.                                               | `9!1.2.3.post4+local` → `9!1.2.3.post4` |
| `release_version`      | Excludes epoch, dev, pre, post, and local.                    | `9!1.2.3.post4` → `1.2.3`      |
| `major`               | The major version number.                                     | `1.2.3` → `1`                  |
| `minor`               | The minor version number.                                     | `1.2.3` → `2`                  |
| `micro`               | The micro version number.                                     | `1.2.3` → `3`                  |
| `patch`               | Alias for `micro`.                                           | `1.2.3` → `3`                  |
| `epoch`               | The epoch string including the `!`. Empty if epoch is `0`.   | `1!2.3` → `1!`                 |
| `epoch_number`        | The epoch number.                                            | `1!2.3` → `1`                  |
| `pre`                 | The pre-release string. Empty if none.                       | `1.2.3a4` → `a4`               |
| `post`                | The post-release string including `.post`. Empty if none.     | `1.2.3.post4` → `.post4`        |
| `post_number`         | The post-release number. Empty if none.                      | `1.2.3.post4` → `4`            |
| `dev`                 | The dev-release string including `.dev`. Empty if none.       | `1.2.3.dev5` → `.dev5`          |
| `dev_number`          | The dev-release number. Empty if none.                       | `1.2.3.dev5` → `5`             |
| `local`               | The local version string including `+`. Empty if none.       | `1.2.3+local` → `+local`       |
| `local_segment`       | The local version segment. Empty if none.                    | `1.2.3+local` → `local`        |
