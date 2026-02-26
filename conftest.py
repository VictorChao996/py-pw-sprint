# Root conftest.py — Global fixtures available to all tests
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Base URL for UI tests."""
    return "https://the-internet.herokuapp.com"


@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for API tests."""
    return "https://jsonplaceholder.typicode.com"
