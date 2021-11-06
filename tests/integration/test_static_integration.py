from cotd.static import StaticReader, Static
import pytest
import pathlib
import sys

@pytest.fixture()
def data():
    test_attibute_path = pathlib.Path("/tmp/file1")
    test_attibute_path.touch(exist_ok=False)
    yield Static(**dict(test_attribute=test_attibute_path))
    test_attibute_path.unlink(missing_ok=False)
    assert test_attibute_path.is_file() == False

@pytest.fixture()
def reader(data: Static):
    return StaticReader(data)


def test_integration_static_reader_returns_repeatable_correct_values(data: Static, reader: StaticReader) -> None:
    """Test file opens and being read multiple times with the same content"""

    res1 = reader.test_attribute.read()
    res1 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()

    assert res1 == res2

if __name__ == "__main__":

    sys.exit(pytest.main(sys.argv[1:]))
