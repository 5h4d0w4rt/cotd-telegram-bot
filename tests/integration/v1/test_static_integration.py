from cotd.static import StaticReader, Static
import pytest
import pathlib
import sys

@pytest.fixture()
def setup_test_file():
    test_attibute_path = pathlib.Path("/tmp/file1")
    try:
        test_attibute_path.touch(exist_ok=False)
    except OSError:
        # recreate file if it's there for some reason (for example pytest crash)
        test_attibute_path.unlink(missing_ok=False)
        test_attibute_path.touch(exist_ok=False)

    # ensure file is indeed empty
    assert test_attibute_path.stat().st_size == 0
    test_attibute_path.write_bytes(b"contents")

    yield test_attibute_path
    teardown_test_file(test_attibute_path)

def teardown_test_file(test_file: pathlib.Path):
    """teardown any state that was previously setup with a setup_function
    call.
    """
    test_file.unlink(missing_ok=False)
    assert test_file.is_file() == False

@pytest.fixture()
def data(setup_test_file: pathlib.Path):
    yield Static(**dict(test_attribute=setup_test_file))

@pytest.fixture()
def reader(data: Static):
    yield StaticReader(data)


def test_integration_static_reader_returns_repeatable_correct_values(data: Static, reader: StaticReader) -> None:
    """Test file opens and being read multiple times with the same content"""

    res1 = reader.test_attribute.read()
    res1 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()
    res2 = reader.test_attribute.read()

    assert res1 == res2

    assert data.test_attribute.read_bytes() == res1

if __name__ == "__main__":

    sys.exit(pytest.main(sys.argv[1:]))
