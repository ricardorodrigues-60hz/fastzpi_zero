import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastzpi_zero.app import app
from fastzpi_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


def session():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
