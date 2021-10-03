from os import stat
from cotd.static import BaseStaticReader
import pytest
import pathlib
from dataclasses import dataclass
import sys
import pyfakefs
import pyfakefs.fake_filesystem
from pyfakefs.fake_filesystem import FakeFile, FakeFileOpen
import io
import typing
import operator

pytest_plugins = ("pyfakefs",)  # this is imported from BUILD bazel file for tests

from pyfakefs.fake_filesystem_unittest import Patcher


@pytest.fixture
def fake_filesystem(
    fs: pyfakefs.fake_filesystem.FakeFilesystem,
) -> pyfakefs.fake_filesystem.FakeFilesystem:  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    this came from pyfakefs http://jmcgeheeiv.github.io/pyfakefs/release/usage.html
    """
    yield fs


@dataclass
class StubStatic:
    test_attribute: FakeFile


class StubStaticReader(BaseStaticReader):
    static: StubStatic
    fake_filesystem: pyfakefs.fake_filesystem.FakeFilesystem

    def __init__(self, static, fake_filesystem) -> None:
        self.static = static
        self.fake_filesystem = fake_filesystem
        super().__init__()

    def __getattribute__(self, name: str) -> typing.BinaryIO:
        fake_filesystem = object.__getattribute__(self, "fake_filesystem")
        fakeOpener = pyfakefs.fake_filesystem.FakeFileOpen(fake_filesystem)

        fake_file: FakeFile = operator.attrgetter(name)(object.__getattribute__(self, "static"))

        return fakeOpener.call("/tmp/file1", "rb")  # type: ignore


@pytest.fixture
def test_data(fs: pyfakefs.fake_filesystem.FakeFilesystem) -> StubStatic:
    return StubStatic(test_attribute=fs.create_file("/tmp/file1", contents="helloworld"))


@pytest.fixture
def reader(fake_filesystem: pyfakefs.fake_filesystem.FakeFilesystem, test_data: StubStatic):
    return StubStaticReader(static=test_data, fake_filesystem=fake_filesystem)


def test_static_reader_returns_repeatable_values(reader: StubStaticReader):
    """Test file opens and being read multiple times with the same content"""
    res1 = reader.test_attribute.read()
    res1 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()

    assert res1 == res2


if __name__ == "__main__":

    sys.exit(pytest.main(sys.argv[1:]))
