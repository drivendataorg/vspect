import argparse
from pathlib import Path
import textwrap

from packaging.version import parse

from vspect import (
    __version__,
    format_version,
    get_package_version,
    read_version_from_pyproject_toml,
)

# create the top-level parser
parser = argparse.ArgumentParser(
    description="Lightweight utility for working with Python package version strings."
)
parser.add_argument("-V", "--version", action="version", version=__version__)
subparsers = parser.add_subparsers(help="Commands")


class IndentedWrapFormatter(argparse.HelpFormatter):
    """Custom formatter that preserves indentation in descriptions."""

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        """Wrap the description while preserving indentation, but leave argument formatting
        unchanged."""
        if self._root_section.heading is None:  # Only modify the top-level description
            wrapped_lines = []
            for line in text.splitlines():
                stripped = line.lstrip()
                if not stripped:
                    wrapped_lines.append("")  # Preserve empty lines
                    continue

                leading_spaces = len(line) - len(stripped)
                effective_indent = " " * (leading_spaces + len(indent))

                # Wrap while respecting the original indentation
                wrapped = textwrap.fill(
                    stripped,
                    width=width - leading_spaces,
                    initial_indent=" " * leading_spaces,
                    subsequent_indent=effective_indent,
                )
                wrapped_lines.append(wrapped)

            return "\n".join(wrapped_lines)

        return super()._fill_text(
            text, width, indent
        )  # Default behavior for everything else


REPLACEMENT_FIELD_HELP = """
The optional format string is passed to str.format(). For example: 'v{major}.{minor}'

Available replacement fields are:

version
  The full version string.
base_version
  The base version string. Excludes dev, pre, post, and local. Example: 1.2.3.post4.dev5 -> 1.2.3
major_minor_version
  The major and minor version string. Example: 1.2.3 -> 1.2
public_version
  The public version string, excludes local. Example: 9!1.2.3.post4+local -> 9!1.2.3.post4
release_version
  The release version string, excludes epoch, dev, pre, post, and local. Example: 9!1.2.3.post4 -> 1.2.3
major
  The major version number. Example: 1.2.3 -> 1
minor
  The minor version number. Example: 1.2.3 -> 2
micro
  The micro version number. Example: 1.2.3 -> 3
patch
  Alias for 'micro'.
epoch
  The epoch string including the '!'. Empty string if epoch is 0. Example: 1!2.3 -> 1!
epoch_number
  The epoch number. Example: 1!2.3 -> 1
pre
  The pre-release string. Empty string if none. Example: 1.2.3a4 -> a4
post
  The post-release string including the '.post'. Empty string if none. Example: 1.2.3.post4 -> post4
post_number
  The post-release number. Empty string if none. Example: 1.2.3.post4 -> 4
dev
  The dev-release string including the '.dev'. Empty string if none. Example: 1.2.3.dev5 -> dev5
dev_number
  The dev-release number. Empty string if none. Example: 1.2.3.dev5 -> 5
local
  The local version string including the '+'. Empty string if none. Example: 1.2.3+local -> +local
local_segment
  The local version segment. Empty string if none. Example: 1.2.3+local -> local
"""  # noqa: E501


def parse_and_format(version: str, format_string: str):
    parsed_version = parse(version)
    print(format_version(parsed_version, format_string))


parse_parser = subparsers.add_parser(
    "parse",
    help="Parse a provided version string and format it.",
    description="Parse a valid PEP 440 version string and format it."
    + "\n\n"
    + REPLACEMENT_FIELD_HELP,
    formatter_class=IndentedWrapFormatter,
)
parse_parser.add_argument("version", help="Version string to parse.")
parse_parser.set_defaults(_func=parse_and_format)


def get_package_version_and_format(package_name: str, format_string: str):
    version = get_package_version(package_name)
    print(format_version(version, format_string))


package_parser = subparsers.add_parser(
    "package",
    help="Get a package's version and format it.",
    description="Get a package's version and format it."
    + "\n\n"
    + REPLACEMENT_FIELD_HELP,
    formatter_class=IndentedWrapFormatter,
)
package_parser.add_argument("package_name", help="Package name to get version of.")
package_parser.set_defaults(_func=get_package_version_and_format)


def read_from_pyproject_toml_and_format(path: str, format_string: str):
    version = read_version_from_pyproject_toml(Path(path))
    print(format_version(version, format_string))


read_parser = subparsers.add_parser(
    "read",
    help="Read a version from a pyproject.toml file and format it.",
    description="Read a version from a pyproject.toml file and format it. "
    + "Requires the version to be statically defined."
    + "\n\n"
    + REPLACEMENT_FIELD_HELP,
    formatter_class=IndentedWrapFormatter,
)
read_parser.add_argument(
    "path", help="File path or directory of a pyproject.toml file."
)
read_parser.set_defaults(_func=read_from_pyproject_toml_and_format)


for subparser in (parse_parser, package_parser, read_parser):
    subparser.add_argument(
        "format_string",
        help="Format string to use for formatting the version. Default: '{version}'",
        default="{version}",
        nargs="?",  # Make positional argument optional
    )


def main():
    args = parser.parse_args()
    if not hasattr(args, "_func"):
        parser.print_help()
        parser.error("No command provided.")
    args._func(**{k: v for k, v in vars(args).items() if k != "_func"})


if __name__ == "__main__":
    main()
