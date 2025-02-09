import importlib.metadata

from packaging.version import Version, parse

__version__ = importlib.metadata.version("vspect")


def get_package_version(package_name: str) -> Version:
    """Get the version of a package.

    Args:
        package_name (str): The name of the package to get the version of.

    Returns:
        packaging.Version: The version of the package.
    """
    return parse(importlib.metadata.version(package_name))


def format_version(version: Version, format_string: str) -> str:
    """Format a version using a format string.

    Args:
        version (packaging.Version): The version to format.
        format_string (str): The format string to use.

    Returns:
        str: The formatted version.
    """
    return format_string.format(
        version=version,
        # alternate forms
        base_version=version.base_version,
        major_minor_version=f"{version.major}.{version.minor}",
        public_version=version.public,
        release_version=".".join(str(comp) for comp in version.release),
        # components
        major=version.major if version.major is not None else version.epoch,
        minor=version.minor if version.minor is not None else version.major,
        micro=version.micro if version.micro is not None else version.patch,
        patch=version.micro if version.micro is not None else version.patch,
        epoch=f"{version.epoch}!" if version.epoch else "",
        epoch_number=version.epoch if version.epoch else "",
        pre=(
            "".join(str(comp) for comp in version.pre)
            if version.pre is not None
            else ""
        ),
        post=f".post{version.post}" if version.post is not None else "",
        post_number=version.post if version.post is not None else "",
        dev=f".dev{version.dev}" if version.dev is not None else "",
        dev_number=version.dev if version.dev is not None else "",
        local=f"+{version.local}" if version.local is not None else "",
        local_segment=version.local if version.local is not None else "",
    )
