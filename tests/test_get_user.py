import pytest

from testing_exercises.get_user import get_os_user_lower


def test_upper_to_lower(mock_env_user):
    assert get_os_user_lower() == "testuser"


def test_raise_exception(mock_env_missing):
    with pytest.raises(OSError):
        _ = get_os_user_lower()
