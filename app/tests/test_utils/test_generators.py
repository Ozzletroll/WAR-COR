import pytest
import io
import builtins
from app.utils import generators


@pytest.fixture
def mock_files(monkeypatch):
    files = {}

    # Save a reference to the original open function
    original_open = builtins.open

    def mock_open(file, mode="r"):

        def is_file_to_mock(file):
            mocked_file_names = ["nouns.json", "adjectives.json", "verbs.json"]
            for filename in mocked_file_names:
                if filename in str(file):
                    return True

        if is_file_to_mock(file):
            file_obj = io.StringIO()
            files[file] = file_obj
            return file_obj
        else:
            return original_open(file, mode)

    monkeypatch.setattr("builtins.open", mock_open)
    yield files


def test_create_data(mock_files):

    generators.create_data()
    files = mock_files
    assert len(files) == 3

    expected_names = ["nouns.json", "adjectives.json", "verbs.json"]

    for file_path, file_object in files.items():
        found = False
        for name in expected_names:
            if name in str(file_path):
                found = True
                break
        assert found
