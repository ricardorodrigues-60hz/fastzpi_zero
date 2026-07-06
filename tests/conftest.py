import pytest
from fastapi.testclient import TestClient

from fastzpi_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)
