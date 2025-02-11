import subprocess
import sys

import pytest

EXECUTABLE = [sys.executable]


def test_help():
    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "--help"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert (
        "Lightweight utility for working with Python package version strings."
        in result.stdout
    )
    assert "Commands" in result.stdout
    assert "parse" in result.stdout
    assert "package" in result.stdout

    # Running with no command prints out help but gives error code
    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode > 0
    assert (
        "Lightweight utility for working with Python package version strings."
        in result.stdout
    )
    assert "Commands" in result.stdout
    assert "parse" in result.stdout
    assert "package" in result.stdout

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "parse", "--help"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Parse a valid PEP 440 version string and format it." in result.stdout

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "package", "--help"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Get a package's version and format it." in result.stdout

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "read", "--help"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Read a version from a pyproject.toml file and format it." in result.stdout


def test_parse():
    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "parse", "1.2.3"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert result.stdout == "1.2.3\n"

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "parse", "1.2.3.post4.dev5"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert result.stdout == "1.2.3.post4.dev5\n"

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "parse", "1.2.3", "{major}.{minor}"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert result.stdout == "1.2\n"


def test_package():
    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "package", "pytest"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert result.stdout == f"{pytest.__version__}\n"

    result = subprocess.run(
        EXECUTABLE + ["-m", "vspect", "package", "pytest", "{major}.{minor}"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    pytest_version_parts = pytest.__version__.split(".")
    assert result.stdout == f"{pytest_version_parts[0]}.{pytest_version_parts[1]}\n"


def test_read():
    result = subprocess.run(
        EXECUTABLE
        + ["-m", "vspect", "read", "tests/assets/pyproject.toml", "{major}.{minor}"],
        capture_output=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert result.stdout == "2020.0\n"
