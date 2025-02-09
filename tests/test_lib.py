from dataclasses import dataclass
from typing import Sequence

from packaging.version import Version
import pytest

from vspect import __version__, format_version, get_package_version


def test_get_package_version():
    vspect_version = get_package_version("vspect")
    assert isinstance(vspect_version, Version)
    assert str(vspect_version) == __version__

    pytest_version = get_package_version("pytest")
    assert isinstance(pytest_version, Version)
    assert isinstance(get_package_version("pytest"), Version)
    assert str(pytest_version) == pytest.__version__


@dataclass
class _TestCaseExpected:
    field_name: str
    expected: str


@dataclass
class _TestCase:
    input: str
    expected: Sequence[_TestCaseExpected]


TEST_CASES = [
    _TestCase(
        input="1.2.3",
        expected=[
            _TestCaseExpected("version", "1.2.3"),
            _TestCaseExpected("major_minor_version", "1.2"),
            _TestCaseExpected("base_version", "1.2.3"),
            _TestCaseExpected("release_version", "1.2.3"),
            _TestCaseExpected("public_version", "1.2.3"),
            _TestCaseExpected("major", "1"),
            _TestCaseExpected("minor", "2"),
            _TestCaseExpected("micro", "3"),
            _TestCaseExpected("patch", "3"),
            _TestCaseExpected("epoch", ""),
            _TestCaseExpected("epoch_number", ""),
            _TestCaseExpected("pre", ""),
            _TestCaseExpected("post", ""),
            _TestCaseExpected("post_number", ""),
            _TestCaseExpected("dev", ""),
            _TestCaseExpected("dev_number", ""),
            _TestCaseExpected("local", ""),
            _TestCaseExpected("local_segment", ""),
        ],
    ),
    _TestCase(
        input="1.2.3.post4.dev5",
        expected=[
            _TestCaseExpected("version", "1.2.3.post4.dev5"),
            _TestCaseExpected("major_minor_version", "1.2"),
            _TestCaseExpected("base_version", "1.2.3"),
            _TestCaseExpected("release_version", "1.2.3"),
            _TestCaseExpected("public_version", "1.2.3.post4.dev5"),
            _TestCaseExpected("major", "1"),
            _TestCaseExpected("minor", "2"),
            _TestCaseExpected("micro", "3"),
            _TestCaseExpected("patch", "3"),
            _TestCaseExpected("epoch", ""),
            _TestCaseExpected("epoch_number", ""),
            _TestCaseExpected("pre", ""),
            _TestCaseExpected("post", ".post4"),
            _TestCaseExpected("post_number", "4"),
            _TestCaseExpected("dev", ".dev5"),
            _TestCaseExpected("dev_number", "5"),
            _TestCaseExpected("local", ""),
            _TestCaseExpected("local_segment", ""),
        ],
    ),
    _TestCase(
        input="9!6.7.9a1+foo",
        expected=[
            _TestCaseExpected("version", "9!6.7.9a1+foo"),
            _TestCaseExpected("major_minor_version", "6.7"),
            _TestCaseExpected("base_version", "9!6.7.9"),
            _TestCaseExpected("release_version", "6.7.9"),
            _TestCaseExpected("public_version", "9!6.7.9a1"),
            _TestCaseExpected("major", "6"),
            _TestCaseExpected("minor", "7"),
            _TestCaseExpected("micro", "9"),
            _TestCaseExpected("patch", "9"),
            _TestCaseExpected("epoch", "9!"),
            _TestCaseExpected("epoch_number", "9"),
            _TestCaseExpected("pre", "a1"),
            _TestCaseExpected("post", ""),
            _TestCaseExpected("post_number", ""),
            _TestCaseExpected("dev", ""),
            _TestCaseExpected("dev_number", ""),
            _TestCaseExpected("local", "+foo"),
            _TestCaseExpected("local_segment", "foo"),
        ],
    ),
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_format_version(test_case):
    version = Version(test_case.input)
    for expected in test_case.expected:
        assert (
            format_version(version, f"{{{expected.field_name}}}") == expected.expected
        ), f"Failed for {expected.field_name}"
