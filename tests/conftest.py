import pytest
import requests


# custom class to be the mock return value of requests.get()
class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_env_user(monkeypatch):
    """Set the USER environment variable to 'TestUser'."""
    monkeypatch.setenv("USER", "TestUser")


@pytest.fixture
def mock_env_missing(monkeypatch):
    """Delete the USER environment variable."""
    monkeypatch.delenv("USER", raising=False)
