from cotd.static import BaseStatic, BaseStaticReader
import pytest
from dataclasses import dataclass
import sys
import pyfakefs
import pyfakefs.fake_filesystem
from pyfakefs.fake_filesystem import AnyFileWrapper, FakeFile, FakeFileOpen, FakeFileWrapper, FakeFilesystem
import operator

pytest_plugins = ("pyfakefs",)  # this is imported from BUILD bazel file for tests


@dataclass
class FakeStatic(BaseStatic):
    test_attribute: FakeFile

    def __init__(self, **kwargs: FakeFile):
        for test_meme in kwargs:
            self.__setattr__(test_meme, kwargs[test_meme])

    def __getattribute__(self, name: str) -> FakeFile:
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: FakeFile) -> None:
        object.__setattr__(self, name, value)

@pytest.fixture
def fake_filesystem(
    fs: FakeFilesystem,
) -> FakeFilesystem:  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    this came from pyfakefs http://jmcgeheeiv.github.io/pyfakefs/release/usage.html
    """
    return fs


class StubStaticReader(BaseStaticReader):
    static: FakeStatic
    fake_filesystem: pyfakefs.fake_filesystem.FakeFilesystem

    def __init__(self, static, fake_filesystem) -> None:
        self.static = static
        self.fake_filesystem = fake_filesystem

    def __getattribute__(self, name: str) -> FakeFileWrapper: # return io.BytesIO-like object
        fake_filesystem = object.__getattribute__(self, "fake_filesystem")
        fakeOpener = pyfakefs.fake_filesystem.FakeFileOpen(fake_filesystem)

        fake_file: FakeFile = operator.attrgetter(name)(object.__getattribute__(self, "static"))

        return fakeOpener.call(fake_file.path, "rb") # type: ignore


@pytest.fixture
def data(fs: pyfakefs.fake_filesystem.FakeFilesystem) -> FakeStatic:
    return FakeStatic(test_attribute=fs.create_file('/tmp/file1', contents=b"contents"))


@pytest.fixture
def reader(fake_filesystem: pyfakefs.fake_filesystem.FakeFilesystem, data: FakeStatic):
    return StubStaticReader(static=data, fake_filesystem=fake_filesystem)


def test_static_attribute_accessable_after_construction(data: FakeStatic) -> None:
    attribute_to_access = 'test_attribute'
    res = getattr(data, attribute_to_access)
    assert type(res) is FakeFile


def test_static_reader_returns_repeatable_correct_values(data: FakeStatic, reader: StubStaticReader) -> None:
    """Test file opens and being read multiple times with the same content"""

    res1 = reader.test_attribute.read()
    res1 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()

    assert res1 == res2
    assert res1 == data.test_attribute.byte_contents
    assert res2 == data.test_attribute.byte_contents


if __name__ == "__main__":

    sys.exit(pytest.main(sys.argv[1:]))
