import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from main import app


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:Postgres123!"
    "@localhost:5432/fastapi_videos_test",
)


test_engine = create_engine(
    TEST_DATABASE_URL
)


TestingSessionLocal = sessionmaker(
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = (
    override_get_db
)


@pytest.fixture(scope="function")
def db():
    database = TestingSessionLocal()

    try:
        yield database
    finally:
        database.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(
        bind=test_engine
    )

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(
        bind=test_engine
    )